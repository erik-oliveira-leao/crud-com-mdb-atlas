import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)


MONGO_USER = os.getenv('MONGO_USER', 'djlau12')
MONGO_PASS = os.getenv('MONGO_PASS', 'fby8oQ6Ytox49W6v')
MONGO_CLUSTER = os.getenv('MONGO_CLUSTER', 'cluster0.x2l20.mongodb.net')
MONGO_DB = os.getenv('MONGO_DB', 'ecommerce')

if not MONGO_PASS:
    raise RuntimeError(
        'A variável de ambiente MONGO_PASS não está definida. Defina a senha do Atlas e rode novamente.'
    )

MONGO_PASS_ENCODED = quote_plus(MONGO_PASS)
MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS_ENCODED}@{MONGO_CLUSTER}/"
    f"{MONGO_DB}?retryWrites=true&w=majority"
)

# Inicializar cliente como None - será conectado sob demanda
client = None
db = None
produtos_collection = None

def get_db():
    """Conecta ao MongoDB sob demanda (lazy connection)"""
    global client, db, produtos_collection
    
    if client is None:
        try:
            client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            db = client[MONGO_DB]
            produtos_collection = db['produtos']
            print("✓ Conectado ao MongoDB Atlas com sucesso!")
        except Exception as exc:
            print(f"✗ Erro ao conectar ao MongoDB Atlas: {exc}")
            raise
    
    return produtos_collection

# Rota para adicionar um novo produto (CREATE)
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    try:
        collection = get_db()
        novo_produto = request.get_json()
        produto_id = collection.insert_one(novo_produto).inserted_id
        return jsonify({"mensagem": "Produto adicionado com sucesso!", "id": str(produto_id)}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para listar todos os produtos (READ)
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    try:
        collection = get_db()
        produtos = list(collection.find())
        for produto in produtos:
            produto['_id'] = str(produto['_id'])
        return jsonify(produtos)
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para buscar um produto por ID (READ)
@app.route('/produtos/<id>', methods=['GET'])
def obter_produto(id):
    try:
        collection = get_db()
        produto = collection.find_one({"_id": ObjectId(id)})
        if produto:
            produto['_id'] = str(produto['_id'])
            return jsonify(produto)
        else:
            return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para atualizar um produto (UPDATE)
@app.route('/produtos/<id>', methods=['PUT'])
def atualizar_produto(id):
    try:
        collection = get_db()
        dados_atualizados = request.get_json()
        resultado = collection.update_one({"_id": ObjectId(id)}, {"$set": dados_atualizados})
        if resultado.matched_count > 0:
            return jsonify({"mensagem": "Produto atualizado com sucesso!"})
        else:
            return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para remover um produto (DELETE)
@app.route('/produtos/<id>', methods=['DELETE'])
def remover_produto(id):
    try:
        collection = get_db()
        resultado = collection.delete_one({"_id": ObjectId(id)})
        if resultado.deleted_count > 0:
            return jsonify({"mensagem": "Produto removido com sucesso!"})
        else:
            return jsonify({"erro": "Produto não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# Rota para a página inicial (Frontend)
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# Rota para servir os arquivos estáticos do frontend
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

