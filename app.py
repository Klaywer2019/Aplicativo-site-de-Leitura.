from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

# --- 🛡️ PONTE DE CRISTAL (CORS) ---
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Rota de teste
@app.route('/')
def home():
    return "🔥 O MOTOR ESTÁ LIGADO! 🔥"

# --- 🆕 ROTA DE LOGIN ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    try:
        # Ajustado para 'usuarios.db' que é o que você criou no terminal
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT nome, email FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({
                "status": "sucesso", 
                "usuario": user[0], 
                "email": user[1]
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
        # Salva o novo cidadão no banco de dados
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "msg": "✨ Alistamento concluído! Agora é só logar."})
    except sqlite3.IntegrityError:
        return jsonify({"status": "erro", "msg": "🚫 Este e-mail já pertence a outro guerreiro!"}), 400
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no portal: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n🚀 REINO CELESTE: AGUARDANDO CONEXÃO NA PORTA 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
