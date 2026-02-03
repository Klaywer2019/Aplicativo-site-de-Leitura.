from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import subprocess

app = Flask(__name__)
CORS(app)

def conectar_banco():
    return sqlite3.connect('reino_celeste.db')

# --- 🧪 ORÁCULO C++: CRIPTO/DESCRIPTO ---
def usar_oraculo_cpp(texto, modo):
    try:
        subprocess.run(['g++', 'runas_seguranca.cpp', '-o', 'oraculo'], check=True)
        processo = subprocess.run(['./oraculo', modo, texto], capture_output=True, text=True)
        return processo.stdout.strip()
    except Exception as e:
        print(f"⚠️ Falha no Oráculo C++: {e}")
        return texto

# --- 🆕 ROTA: CADASTRAR NOVO MESTRE ---
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "msg": "✨ Cadastro Realizado! Agora faça login."})
    except Exception as e:
        return jsonify({"status": "erro", "msg": "E-mail já existe no Reino!"}), 400

# --- 🆕 ROTA: LOGIN (CHAMA O GUARDIÃO JAVA) ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')

    try:
        # O Python grita pro Java: "Ei, esse email e senha batem?"
        subprocess.run(['javac', 'ValidadorReal.java'], check=True)
        validacao = subprocess.run(['java', 'ValidadorReal', 'login', email, senha], capture_output=True, text=True)
        
        if "autorizado" in validacao.stdout.lower():
            # Pegamos o nome que o Java achou no banco
            nome_user = validacao.stdout.split(":")[1].strip()
            return jsonify({"status": "sucesso", "msg": f"Bem-vindo, {nome_user}!", "usuario": nome_user})
        else:
            return jsonify({"status": "erro", "msg": "🚫 Acesso Negado: Dados incorretos!"}), 401
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no Guardião: {e}"}), 500

@app.route('/salvar_tesouro', methods=['POST'])
def salvar_tesouro():
    dados = request.json
    usuario = dados.get('usuario')
    codigo_puro = dados.get('codigo')

    # Validação simples com Java antes de salvar
    try:
        subprocess.run(['javac', 'ValidadorReal.java'], check=True)
        validacao = subprocess.run(['java', 'ValidadorReal', 'autorizar', usuario], capture_output=True, text=True)
        if "autorizado" not in validacao.stdout.lower():
            return jsonify({"status": "erro", "msg": "🚫 Bloqueado pelo Guardião!"}), 403
    except Exception:
        return jsonify({"status": "erro", "msg": "Erro de segurança"}), 500

    codigo_selado = usar_oraculo_cpp(codigo_puro, 'c')

    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tesouros (usuario, codigo) VALUES (?, ?)", (usuario, codigo_selado))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "msg": "✅ Tesouro salvo!"})
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)}), 500

@app.route('/listar_tesouros', methods=['GET'])
def listar_tesouros():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, codigo, data_criacao FROM tesouros ORDER BY data_criacao DESC")
        linhas = cursor.fetchall()
        conn.close()
        tesouros_limpos = [{"usuario": u, "codigo": usar_oraculo_cpp(c, 'd'), "data": d} for u, c, d in linhas]
        return jsonify(tesouros_limpos)
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)}), 500

if __name__ == '__main__':
    print("\n🔥 MOTOR ULTRA LIGADO: LOGIN | CADASTRO | FORJA | INVENTÁRIO 🔥\n")
    app.run(port=5000, debug=True)
