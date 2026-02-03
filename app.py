From flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import subprocess
import os
import platform

app = Flask(__name__)

# --- 🛡️ ACESSO TOTAL (GITHUB PAGES) ---
CORS(app, resources={r"/*": {"origins": "*"}}) 

def conectar_banco():
    return sqlite3.connect('reino_celeste.db')

# --- 🛠️ INICIALIZADOR DO REINO ---
def inicializar_reino():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                sigla TEXT DEFAULT '[Explorador-🛡️]'
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tesouros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                codigo TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"❌ Erro ao iniciar banco: {e}")
    finally:
        conn.close()

# --- 🧪 ORÁCULO C++: CRIPTO/DESCRIPTO ---
def usar_oraculo_cpp(texto, modo):
    # Ajuste para Windows (adiciona .exe se necessário)
    ext = ".exe" if platform.system() == "Windows" else ""
    nome_binario = f"./oraculo{ext}"
    
    try:
        if not os.path.exists(nome_binario):
            print("🔨 Compilando Oráculo C++...")
            subprocess.run(['g++', 'runas_seguranca.cpp', '-o', f'oraculo{ext}'], check=False, shell=True) 
        
        processo = subprocess.run([nome_binario, modo, texto], capture_output=True, text=True, shell=True)
        return processo.stdout.strip()
    except Exception as e:
        print(f"⚠️ Falha no Oráculo C++: {e}")
        return texto

# --- 🆕 ROTA: CADASTRAR NOVO MESTRE ---
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json
    nome, email, senha = dados.get('nome'), dados.get('email'), dados.get('senha')
    
    if not all([nome, email, senha]):
        return jsonify({"status": "erro", "msg": "Preencha todas as runas!"}), 400

    conn = conectar_banco()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha, sigla) VALUES (?, ?, ?, ?)", 
                       (nome, email, senha, "[Explorador-🛡️]"))
        conn.commit()
        return jsonify({"status": "sucesso", "msg": "✨ Cadastro Realizado! Agora faça login."})
    except sqlite3.IntegrityError:
        return jsonify({"status": "erro", "msg": "E-mail já existe no Reino!"}), 400
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no Reino: {str(e)}"}), 500
    finally:
        conn.close()

# --- 🆕 ROTA: LOGIN (GUARDIÃO JAVA) ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email, senha = dados.get('email'), dados.get('senha')
    try:
        # Tenta compilar o Java (apenas se necessário ou toda vez para garantir)
        subprocess.run(['javac', 'ValidadorReal.java'], check=True, shell=True)
        validacao = subprocess.run(['java', 'ValidadorReal', 'login', email, senha], capture_output=True, text=True, shell=True)
        
        if "autorizado" in validacao.stdout.lower():
            # Pega o nome após os dois pontos
            nome_user = validacao.stdout.split(":")[1].strip() if ":" in validacao.stdout else "Mestre"
            return jsonify({"status": "sucesso", "msg": f"Bem-vindo, {nome_user}!", "usuario": nome_user, "email": email})
        else:
            return jsonify({"status": "erro", "msg": "🚫 Dados incorretos!"}), 401
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no Guardião: {e}"}), 500

# --- 🆕 ROTA: BUSCAR PERFIL ---
@app.route('/meu_perfil/<email>', methods=['GET'])
def meu_perfil(email):
    conn = conectar_banco()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT nome, email, senha, sigla FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"status": "erro", "msg": "Mestre não encontrado!"}), 404

        nome_usuario = user[0]
        cursor.execute("SELECT codigo, data_criacao FROM tesouros WHERE usuario = ?", (nome_usuario,))
        obras = cursor.fetchall()

        lista_obras = [{"codigo": usar_oraculo_cpp(o[0], 'd'), "data": o[1]} for o in obras]

        return jsonify({
            "nome": user[0], "email": user[1], "senha": user[2], 
            "sigla": user[3], "obras": lista_obras
        })
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)}), 500
    finally:
        conn.close()

# --- ROTAS DE TESOUROS ---
@app.route('/salvar_tesouro', methods=['POST'])
def salvar_tesouro():
    dados = request.json
    usuario, codigo_puro = dados.get('usuario'), dados.get('codigo')
    
    try:
        # Chama o Java para autorizar
        validacao = subprocess.run(['java', 'ValidadorReal', 'autorizar', usuario], capture_output=True, text=True, shell=True)
        if "autorizado" not in validacao.stdout.lower():
            return jsonify({"status": "erro", "msg": "🚫 Bloqueado pelo Guardião!"}), 403
    except Exception:
        return jsonify({"status": "erro", "msg": "Erro de segurança"}), 500

    codigo_selado = usar_oraculo_cpp(codigo_puro, 'c')
    conn = conectar_banco()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tesouros (usuario, codigo) VALUES (?, ?)", (usuario, codigo_selado))
        conn.commit()
        return jsonify({"status": "sucesso", "msg": "✅ Tesouro salvo!"})
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)}), 500
    finally:
        conn.close()

@app.route('/listar_tesouros', methods=['GET'])
def listar_tesouros():
    conn = conectar_banco()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, codigo, data_criacao FROM tesouros ORDER BY data_criacao DESC")
        linhas = cursor.fetchall()
        tesouros_limpos = [{"usuario": u, "codigo": usar_oraculo_cpp(c, 'd'), "data": d} for u, c, d in linhas]
        return jsonify(tesouros_limpos)
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    inicializar_reino()
    print("\n🔥 MOTOR ULTRA LIGADO: PERFIL E CADASTRO ATIVOS 🔥")
    print("📡 Porta: 5000 | Aguardando sinais...\n")
    app.run(host='0.0.0.0', port=5000, debug=True)