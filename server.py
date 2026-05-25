import os
import logging
from flask import Flask, send_from_directory, jsonify, request
from api import MongoAPI

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
mongo = MongoAPI()


def ensure_connected():
    """Tenta conectar ao MongoDB se ainda não estiver conectado."""
    if mongo.collection is None:
        logger.info("Iniciando conexão com o MongoDB...")
        return mongo.connect()
    return True


# ---------------------------------------------------------------------------
# Rotas de arquivos estáticos
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)


# ---------------------------------------------------------------------------
# API – /produtos
# ---------------------------------------------------------------------------

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    try:
        if not ensure_connected():
            return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 503
        produtos = mongo.listar_produtos()
        if produtos is None:
            return jsonify({'erro': 'Erro ao listar produtos'}), 500
        logger.debug(f"Listando {len(produtos)} produto(s)")
        return jsonify(produtos), 200
    except Exception as e:
        logger.exception("Erro inesperado em GET /produtos")
        return jsonify({'erro': str(e)}), 500


@app.route('/produtos', methods=['POST'])
def adicionar_produto():
    try:
        if not ensure_connected():
            return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 503
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Corpo da requisição inválido ou ausente'}), 400
        produto_id = mongo.adicionar_produto(dados)
        if produto_id is None:
            return jsonify({'erro': 'Erro ao adicionar produto'}), 500
        logger.debug(f"Produto adicionado com id={produto_id}")
        return jsonify({'mensagem': 'Produto adicionado com sucesso', 'id': produto_id}), 201
    except Exception as e:
        logger.exception("Erro inesperado em POST /produtos")
        return jsonify({'erro': str(e)}), 500


@app.route('/produtos/<string:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    try:
        if not ensure_connected():
            return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 503
        produto = mongo.obter_produto(produto_id)
        if produto is None:
            return jsonify({'erro': 'Produto não encontrado'}), 404
        logger.debug(f"Produto obtido: id={produto_id}")
        return jsonify(produto), 200
    except Exception as e:
        logger.exception(f"Erro inesperado em GET /produtos/{produto_id}")
        return jsonify({'erro': str(e)}), 500


@app.route('/produtos/<string:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    try:
        if not ensure_connected():
            return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 503
        dados = request.get_json()
        if not dados:
            return jsonify({'erro': 'Corpo da requisição inválido ou ausente'}), 400
        atualizado = mongo.atualizar_produto(produto_id, dados)
        if not atualizado:
            return jsonify({'erro': 'Produto não encontrado ou sem alterações'}), 404
        logger.debug(f"Produto atualizado: id={produto_id}")
        return jsonify({'mensagem': 'Produto atualizado com sucesso'}), 200
    except Exception as e:
        logger.exception(f"Erro inesperado em PUT /produtos/{produto_id}")
        return jsonify({'erro': str(e)}), 500


@app.route('/produtos/<string:produto_id>', methods=['DELETE'])
def remover_produto(produto_id):
    try:
        if not ensure_connected():
            return jsonify({'erro': 'Não foi possível conectar ao banco de dados'}), 503
        removido = mongo.remover_produto(produto_id)
        if not removido:
            return jsonify({'erro': 'Produto não encontrado'}), 404
        logger.debug(f"Produto removido: id={produto_id}")
        return jsonify({'mensagem': 'Produto removido com sucesso'}), 200
    except Exception as e:
        logger.exception(f"Erro inesperado em DELETE /produtos/{produto_id}")
        return jsonify({'erro': str(e)}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    logger.info(f"Iniciando servidor na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)

