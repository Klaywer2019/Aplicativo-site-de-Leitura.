from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função pra conectar no banco SQL
def conectar_banco():
    return sqlite3.connect('reino_celeste.db')

@app.route('/salvar_tesouro', methods=['POST'])
def salvar_tesouro():
    dados = request.json
    usuario = dados.get('usuario')
    codigo = dados.get('codigo')
    
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tesouros (usuario, codigo) VALUES (?, ?)", (usuario, codigo))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "sucesso", "msg": "Tesouro guardado no cofre real!"})

if __name__ == '__main__':
    app.run(debug=True)
