from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

# --- 🛡️ PONTE DE CRISTAL (CORS) ---
# Isso libera o acesso para o seu site no GitHub não ser bloqueado
CORS(app, resources={r"/*": {"origins": "*"}}) 

# Rota de teste que você já criou
@app.route('/')
def home():
    return "🔥 O MOTOR ESTÁ LIGADO! 🔥"

# --- 🆕 ROTA DE LOGIN (O que o seu index.html precisa) ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    try:
        conn = sqlite3.connect('reino_celeste.db')
        cursor = conn.cursor()
        # Procura o mestre no cofre que você criou com o db_manager
        cursor.execute("SELECT nome, email FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Se achou, manda o sinal de sucesso pro index.html
            return jsonify({
                "status": "sucesso", 
                "usuario": user[0], 
                "email": user[1]
            })
        else:
            return jsonify({"status": "erro", "msg": "🚫 Dados incorretos ou não cadastrados!"}), 401
            
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no banco: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n🚀 REINO CELESTE: AGUARDANDO CONEXÃO NA PORTA 5000...")
    # O host 0.0.0.0 é fundamental para o GitHub Pages te encontrar
    app.run(host='0.0.0.0', port=5000, debug=True)
