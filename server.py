import os
import sys
from urllib.parse import quote_plus
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)

MONGO_USER = os.getenv('MONGO_USER', 'djlau12')
MONGO_PASS = os.getenv('MONGO_PASS', 'fby8oQ6Ytox49W6v')
MONGO_CLUSTER = os.getenv('MONGO_CLUSTER', 'cluster0.x2l20.mongodb.net')
MONGO_DB = os.getenv('MONGO_DB', 'ecommerce')

# Variáveis globais para conexão
_client = None
_db = None
_collection = None

def get_collection():
    """Obtém a coleção do MongoDB, conectando se necessário"""
    global _client, _db, _collection
    
    if _collection is None:
        try:
            MONGO_PASS_ENCODED = quote_plus(MONGO_PASS)
            MONGO_URI = (
                f"mongodb+srv://{MONGO_USER}:{MONGO_PASS_ENCODED}@{MONGO_CLUSTER}/"
                f"{MONGO_DB}?retryWrites=true&w=majority"
            )
            _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            _client.admin.command('ping')
            _db = _client[MONGO_DB]
            _collection = _db['produtos']
            print("✓ Conectado ao MongoDB", file=sys.stderr)
        except Exception as e:
            print(f"✗ Erro ao conectar ao MongoDB: {e}", file=sys.stderr)
            return None
    
    return _collection

@app.route('/')
def index():
    try:
        return send_from_directory('frontend', 'index.html')
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/<path:filename>')
def serve_static(filename):
    try:
        return send_from_directory('frontend', filename)
    except Exception as e:
        return jsonify({"erro": str(e)}), 404

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"erro": "Conexão com MongoDB indisponível"}), 503
        
        produtos = list(collection.find())
        for produto in produtos:
            produto['_id'] = str(produto['_id'])
        return jsonify(produtos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"erro": "Conexão com MongoDB indisponível"}), 503
        
        novo_produto = request.get_json()
        produto_id = collection.insert_one(novo_produto).inserted_id
        return jsonify({"mensagem": "Produto adicionado com sucesso!", "id": str(produto_id)}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/produtos/<id>', methods=['GET'])
def obter_produto(id):
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"erro": "Conexão com MongoDB indisponível"}), 503
        
        produto = collection.find_one({"_id": ObjectId(id)})
        if produto:
            produto['_id'] = str(produto['_id'])
            return jsonify(produto)
        return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/produtos/<id>', methods=['PUT'])
def atualizar_produto(id):
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"erro": "Conexão com MongoDB indisponível"}), 503
        
        dados_atualizados = request.get_json()
        resultado = collection.update_one({"_id": ObjectId(id)}, {"$set": dados_atualizados})
        if resultado.matched_count > 0:
            return jsonify({"mensagem": "Produto atualizado com sucesso!"})
        return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route('/produtos/<id>', methods=['DELETE'])
def remover_produto(id):
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"erro": "Conexão com MongoDB indisponível"}), 503
        
        resultado = collection.delete_one({"_id": ObjectId(id)})
        if resultado.deleted_count > 0:
            return jsonify({"mensagem": "Produto removido com sucesso!"})
        return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == '__main__':
    print("Iniciando Flask em 0.0.0.0:8000", file=sys.stderr)
    sys.stderr.flush()
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)

