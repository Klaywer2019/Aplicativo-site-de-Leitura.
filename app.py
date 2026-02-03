from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import subprocess
import os
import platform

app = Flask(__name__)

# --- 🛡️ CONFIGURAÇÃO DE ACESSO TOTAL ---
# Isso permite que o GitHub Pages (HTTPS) fale com seu PC (HTTP)
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}}) 

# O RESTANTE DO SEU CÓDIGO (conectar_banco, rotas, etc) SEGUE IGUAL...
# ...
