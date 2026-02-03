from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import subprocess

app = Flask(__name__)
CORS(app)

def conectar_banco():
    return sqlite3.connect('reino_celeste.db')

# --- 🧪 ORÁCULO C++: A PONTE DE PERFORMANCE ---
# Agora ele aceita um modo: 'c' para criptografar e 'd' para descriptografar
def usar_oraculo_cpp(texto, modo):
    try:
        # Garante que o Oráculo está compilado
        subprocess.run(['g++', 'runas_seguranca.cpp', '-o', 'oraculo'], check=True)
        # Executa passando o modo e o texto
        processo = subprocess.run(['./oraculo', modo, texto], capture_output=True, text=True)
        return processo.stdout.strip()
    except Exception as e:
        print(f"⚠️ Falha no Oráculo C++: {e}")
        return texto

@app.route('/salvar_tesouro', methods=['POST'])
def salvar_tesouro():
    dados = request.json
    usuario = dados.get('usuario')
    codigo_puro = dados.get('codigo')

    print(f"--- 🛡️ Iniciando Protocolo Ultra para: {usuario} ---")

    # 1. ☕ VALIDAÇÃO JAVA
    try:
        subprocess.run(['javac', 'ValidadorReal.java'], check=True)
        validacao = subprocess.run(['java', 'ValidadorReal', usuario], capture_output=True, text=True)
        if "autorizado" not in validacao.stdout.lower():
            return jsonify({"status": "erro", "msg": "🚫 Bloqueado pelo Guardião Java!"}), 403
    except Exception as e:
        return jsonify({"status": "erro", "msg": "Erro no sistema de segurança Java"}), 500

    # 2. 💎 CRIPTOGRAFIA C++ (Modo 'c')
    print("🔮 Criptografando com C++...")
    codigo_selado = usar_oraculo_cpp(codigo_puro, 'c')

    # 3. 🗄️ ARMAZENAMENTO SQL
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tesouros (usuario, codigo) VALUES (?, ?)", (usuario, codigo_selado))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "msg": "✅ Tesouro salvo!"})
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no SQL: {e}"}), 500

# --- 🏛️ NOVA ROTA: SALÃO DE LEITURA ---
@app.route('/listar_tesouros', methods=['GET'])
def listar_tesouros():
    try:
        print("📜 Abrindo o Salão de Leitura...")
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT usuario, codigo, data_criacao FROM tesouros ORDER BY data_criacao DESC")
        linhas = cursor.fetchall()
        conn.close()

        tesouros_limpos = []
        for usuario, codigo_cripto, data in linhas:
            # 🔓 DESCRIPTOGRAFIA C++ (Modo 'd')
            # O Python pede pro C++ limpar o código pro site entender
            codigo_aberto = usar_oraculo_cpp(codigo_cripto, 'd')
            
            tesouros_limpos.append({
                "usuario": usuario,
                "codigo": codigo_aberto,
                "data": data
            })

        return jsonify(tesouros_limpos)
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*40)
    print("🔥 SOFTWARE ULTRA REINO CELESTE ATIVADO 🔥")
    print("ESTADO: Python + Java + C++ + SQL conectados!")
    print("ROTAS: /salvar_tesouro | /listar_tesouros")
    print("="*40 + "\n")
    app.run(port=5000, debug=True)
