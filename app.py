from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import subprocess

app = Flask(__name__)
CORS(app)

def conectar_banco():
    return sqlite3.connect('reino_celeste.db')

# --- 🧪 ORÁCULO C++: A PONTE DE PERFORMANCE ---
def usar_oraculo_cpp(texto_original):
    try:
        # Compila o C++ (O mestre das runas)
        subprocess.run(['g++', 'runas_seguranca.cpp', '-o', 'oraculo'], check=True)
        # Executa e pega o texto criptografado
        processo = subprocess.run(['./oraculo', texto_original], capture_output=True, text=True)
        return processo.stdout.strip()
    except Exception as e:
        print(f"⚠️ Falha no Oráculo C++: {e}")
        return texto_original # Fallback: salva original se o C++ falhar

@app.route('/salvar_tesouro', methods=['POST'])
def salvar_tesouro():
    dados = request.json
    usuario = dados.get('usuario')
    codigo_puro = dados.get('codigo')

    print(f"--- 🛡️ Iniciando Protocolo Ultra para: {usuario} ---")

    # 1. ☕ VALIDAÇÃO JAVA (Segurança de Acesso)
    try:
        subprocess.run(['javac', 'ValidadorReal.java'], check=True)
        validacao = subprocess.run(['java', 'ValidadorReal', usuario], capture_output=True, text=True)
        
        if "autorizado" not in validacao.stdout.lower():
            return jsonify({"status": "erro", "msg": "🚫 Bloqueado pelo Guardião Java!"}), 403
    except Exception as e:
        return jsonify({"status": "erro", "msg": "Erro no sistema de segurança Java"}), 500

    # 2. 💎 CRIPTOGRAFIA C++ (Proteção do Conteúdo)
    print("🔮 Chamando Oráculo C++ para selar o código...")
    codigo_selado = usar_oraculo_cpp(codigo_puro)

    # 3. 🗄️ ARMAZENAMENTO SQL (O Cofre Permanente)
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        # Salvamos o código já criptografado pelo C++!
        cursor.execute("INSERT INTO tesouros (usuario, codigo) VALUES (?, ?)", (usuario, codigo_selado))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "msg": "✅ Tesouro criptografado e salvo no SQL!"})
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no SQL: {e}"}), 500

if __name__ == '__main__':
    print("\n" + "="*40)
    print("🔥 SOFTWARE ULTRA REINO CELESTE ATIVADO 🔥")
    print("ESTADO: Python + Java + C++ + SQL conectados!")
    print("="*40 + "\n")
    app.run(port=5000, debug=True)
