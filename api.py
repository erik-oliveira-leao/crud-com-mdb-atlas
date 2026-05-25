"""
API para operações com MongoDB
Configure as variáveis de ambiente antes de usar:
- MONGO_USER
- MONGO_PASS
- MONGO_CLUSTER
- MONGO_DB
"""

import os
from urllib.parse import quote_plus
from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoAPI:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
    
    def connect(self):
        """Conecta ao MongoDB Atlas"""
        try:
            mongo_user = os.getenv('MONGO_USER')
            mongo_pass = os.getenv('MONGO_PASS')
            mongo_cluster = os.getenv('MONGO_CLUSTER')
            mongo_db = os.getenv('MONGO_DB')
            
            if not all([mongo_user, mongo_pass, mongo_cluster, mongo_db]):
                raise ValueError("Variáveis de ambiente MongoDB não configuradas")
            
            mongo_pass_encoded = quote_plus(mongo_pass)
            mongo_uri = (
                f"mongodb+srv://{mongo_user}:{mongo_pass_encoded}@{mongo_cluster}/"
                f"{mongo_db}?retryWrites=true&w=majority"
            )
            
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[mongo_db]
            self.collection = self.db['produtos']
            print("✓ Conectado ao MongoDB com sucesso")
            return True
        except Exception as e:
            print(f"✗ Erro ao conectar ao MongoDB: {e}")
            return False
    
    def listar_produtos(self):
        """Lista todos os produtos"""
        if not self.collection:
            return None
        
        produtos = list(self.collection.find())
        for produto in produtos:
            produto['_id'] = str(produto['_id'])
        return produtos
    
    def obter_produto(self, produto_id):
        """Obtém um produto por ID"""
        if not self.collection:
            return None
        
        try:
            produto = self.collection.find_one({"_id": ObjectId(produto_id)})
            if produto:
                produto['_id'] = str(produto['_id'])
            return produto
        except Exception as e:
            print(f"Erro ao obter produto: {e}")
            return None
    
    def adicionar_produto(self, dados):
        """Adiciona um novo produto"""
        if not self.collection:
            return None
        
        try:
            resultado = self.collection.insert_one(dados)
            return str(resultado.inserted_id)
        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")
            return None
    
    def atualizar_produto(self, produto_id, dados):
        """Atualiza um produto"""
        if not self.collection:
            return False
        
        try:
            resultado = self.collection.update_one(
                {"_id": ObjectId(produto_id)},
                {"$set": dados}
            )
            return resultado.matched_count > 0
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")
            return False
    
    def remover_produto(self, produto_id):
        """Remove um produto"""
        if not self.collection:
            return False
        
        try:
            resultado = self.collection.delete_one({"_id": ObjectId(produto_id)})
            return resultado.deleted_count > 0
        except Exception as e:
            print(f"Erro ao remover produto: {e}")
            return False

