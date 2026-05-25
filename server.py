import os
import logging
from flask import Flask, send_from_directory, jsonify

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200


# ---------------------------------------------------------------------------
# Arquivos estáticos
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    try:
        logger.debug("Servindo index.html")
        return send_from_directory('frontend', 'index.html')
    except Exception as e:
        logger.exception("Erro ao servir index.html")
        return jsonify({'erro': str(e)}), 500


@app.route('/<path:filename>')
def serve_static(filename):
    try:
        logger.debug(f"Servindo arquivo estático: {filename}")
        return send_from_directory('frontend', filename)
    except Exception as e:
        logger.exception(f"Erro ao servir arquivo: {filename}")
        return jsonify({'erro': str(e)}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    logger.info(f"Iniciando servidor na porta {port}")
    app.run(host='0.0.0.0', port=port, debug=False)


