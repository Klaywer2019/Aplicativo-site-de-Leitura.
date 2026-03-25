from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

# --- 🛡️ PONTE DE CRISTAL (CORS) ---
# Liberando para que o navegador aceite as requisições do seu site
CORS(app) 

# --- 🏗️ CONSTRUTOR DE REINO (DATABASE) ---
def init_db():
    """Cria o banco e a tabela se não existirem ao iniciar"""
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Rota de teste
@app.route('/')
def home():
    return "🔥 O MOTOR DO REINO CELESTE ESTÁ LIGADO! 🔥"

# --- 🆕 ROTA DE LOGIN ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        # Busca o guerreiro nas runas do banco
        cursor.execute("SELECT nome, email FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({
                "status": "sucesso", 
                "usuario": user[0], 
                "email": user[1],
                "msg": "✨ Acesso ao Cofre autorizado!"
            })
        else:
            return jsonify({"status": "erro", "msg": "🚫 Dados incorretos ou não cadastrados!"}), 401
            
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no banco: {str(e)}"}), 500

# --- 🖋️ ROTA DE ALISTAMENTO (CADASTRO) ---
@app.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')

    if not nome or not email or not senha:
        return jsonify({"status": "erro", "msg": "Preencha todas as runas de cadastro!"}), 400

    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "msg": "✨ Alistamento concluído! O portal está aberto para você."})
    except sqlite3.IntegrityError:
        return jsonify({"status": "erro", "msg": "🚫 Este e-mail já pertence a outro guerreiro!"}), 400
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no portal: {str(e)}"}), 500

if __name__ == '__main__':
    init_db() # Liga os alicerces do banco
    print("\n🚀 REINO CELESTE: AGUARDANDO CONEXÃO NA PORTA 5000...")
    # host='0.0.0.0' é essencial para funcionar no Codespaces ou Nuvem
    app.run(host='0.0.0.0', port=5000, debug=True)