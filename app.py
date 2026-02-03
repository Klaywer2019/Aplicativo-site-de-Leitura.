from flask import Flask, request, jsonify
from flask_cors import CORS # Importante para o site conseguir falar com o Python
import sqlite3
import subprocess

app = Flask(__name__)
CORS(app) # Isso permite que seu HTML fale com o Python sem bloqueios

# Função para conectar ao Cofre SQL
def conectar_banco():
    return sqlite3.connect('reino_celeste.db')

@app.route('/salvar_tesouro', methods=['POST'])
def salvar_tesouro():
    dados = request.json
    usuario = dados.get('usuario')
    codigo = dados.get('codigo')

    print(f"--- 🛡️ Tentativa de Selar Tesouro: {usuario} ---")

    # ☕ Chamando o Guardião Java (ValidadorReal.java)
    # O Python dá um grito no Java pra ver se você é a criadora
    try:
        # Primeiro compilamos (garante que tá atualizado)
        subprocess.run(['javac', 'ValidadorReal.java'], check=True)
        # Depois rodamos passando o nome do usuário
        resultado_java = subprocess.run(['java', 'ValidadorReal', usuario], capture_output=True, text=True)
        
        if "autorizado" not in resultado_java.stdout.lower():
            return jsonify({"status": "erro", "msg": "Acesso negado pelo Guardião Java!"}), 403
    except Exception as e:
        print(f"Erro ao chamar o Java: {e}")
        # Se o Java falhar, por segurança, a gente não deixa passar no modo Ultra!

    # 🗄️ Salvando no SQL
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tesouros (usuario, codigo) VALUES (?, ?)", (usuario, codigo))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "msg": "Tesouro guardado no SQL!"})
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)}), 500

if __name__ == '__main__':
    print("🔥 MOTOR DO REINO CELESTE LIGADO NA PORTA 5000 🔥")
    app.run(port=5000, debug=True)
