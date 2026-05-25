import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__)


MONGO_USER = os.getenv('MONGO_USER', 'djlau12') #troque 'djlau12' pelo seu nome de usuário do Atlas, ou defina a variável de ambiente MONGO_USER
MONGO_PASS = os.getenv('MONGO_PASS', 'fby8oQ6Ytox49W6v') #troque 'fby8oQ6Ytox49W6v' pela sua senha do Atlas, ou defina a variável de ambiente MONGO_PASS
MONGO_CLUSTER = os.getenv('MONGO_CLUSTER', 'cluster0.x2l20.mongodb.net') #troque 'cluster0.x2l20.mongodb.net' pelo endereço do seu cluster no Atlas, ou defina a variável de ambiente MONGO_CLUSTER
MONGO_DB = os.getenv('MONGO_DB', 'ecommerce') #troque 'ecommerce' pelo nome do seu banco de dados no Atlas, ou defina a variável de ambiente MONGO_DB

if not MONGO_PASS:
    raise RuntimeError(
        'A variável de ambiente MONGO_PASS não está definida. Defina a senha do Atlas e rode novamente.'
    )

MONGO_PASS_ENCODED = quote_plus(MONGO_PASS)
MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASS_ENCODED}@{MONGO_CLUSTER}/"
    f"{MONGO_DB}?retryWrites=true&w=majority"
)

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
try:
    client.admin.command('ping')
except Exception as exc:
    raise RuntimeError(f'Erro ao conectar ao MongoDB Atlas: {exc}') from exc

db = client[MONGO_DB]
produtos_collection = db['produtos']




# Rota para adicionar um novo produto (CREATE)
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    novo_produto = request.get_json()
    produto_id = produtos_collection.insert_one(novo_produto).inserted_id
    return jsonify({"mensagem": "Produto adicionado com sucesso!", "id": str(produto_id)}), 201

# Rota para listar todos os produtos (READ)
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = list(produtos_collection.find())
    for produto in produtos:
        produto['_id'] = str(produto['_id'])  # Converter ObjectId para string
    return jsonify(produtos)

# Rota para buscar um produto por ID (READ)
@app.route('/produtos/<id>', methods=['GET'])
def obter_produto(id):
    produto = produtos_collection.find_one({"_id": ObjectId(id)})
    if produto:
        produto['_id'] = str(produto['_id'])
        return jsonify(produto)
    else:
        return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para atualizar um produto (UPDATE)
@app.route('/produtos/<id>', methods=['PUT'])
def atualizar_produto(id):
    dados_atualizados = request.get_json()
    resultado = produtos_collection.update_one({"_id": ObjectId(id)}, {"$set": dados_atualizados})
    if resultado.matched_count > 0:
        return jsonify({"mensagem": "Produto atualizado com sucesso!"})
    else:
        return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para remover um produto (DELETE)
@app.route('/produtos/<id>', methods=['DELETE'])
def remover_produto(id):
    resultado = produtos_collection.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count > 0:
        return jsonify({"mensagem": "Produto removido com sucesso!"})
    else:
        return jsonify({"erro": "Produto não encontrado"}), 404

# Rota para a página inicial (Frontend)
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

# Rota para servir os arquivos estáticos do frontend
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

if __name__ == '__main__':
    app.run(debug=True)

