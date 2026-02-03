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
        # Nota: Ideal compilar uma vez fora do loop, mas mantive sua lógica original
        subprocess.run(['g++', 'runas_seguranca.cpp', '-o', 'oraculo'], check=False) 
        processo = subprocess.run(['./oraculo', modo, texto], capture_output=True, text=True)
        return processo.stdout.strip()
    except Exception as e:
        print(f"⚠️ Falha no Oráculo C++: {e}")
        return texto

# --- 🆕 ROTA: CADASTRAR NOVO MESTRE (Ajustada) ---
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    
    if not nome or not email or not senha:
        return jsonify({"status": "erro", "msg": "Preencha todas as runas!"}), 400

    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        # Adicionamos a 'sigla' padrão para novos membros
        cursor.execute("INSERT INTO usuarios (nome, email, senha, sigla) VALUES (?, ?, ?, ?)", 
                       (nome, email, senha, "[Explorador-🛡️]"))
        conn.commit()
        conn.close()
        return jsonify({"status": "sucesso", "msg": "✨ Cadastro Realizado! Agora faça login."})
    except Exception as e:
        return jsonify({"status": "erro", "msg": "E-mail já existe no Reino ou Tabela incompleta!"}), 400

# --- 🆕 ROTA: LOGIN (CHAMA O GUARDIÃO JAVA) ---
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    try:
        # Garante que o Java está compilado
        subprocess.run(['javac', 'ValidadorReal.java'], check=True)
        validacao = subprocess.run(['java', 'ValidadorReal', 'login', email, senha], capture_output=True, text=True)
        
        if "autorizado" in validacao.stdout.lower():
            # O Java retorna "Autorizado: NomeDoUsuario"
            nome_user = validacao.stdout.split(":")[1].strip()
            return jsonify({
                "status": "sucesso", 
                "msg": f"Bem-vindo, {nome_user}!", 
                "usuario": nome_user, 
                "email": email
            })
        else:
            return jsonify({"status": "erro", "msg": "🚫 Acesso Negado: Dados incorretos!"}), 401
    except Exception as e:
        return jsonify({"status": "erro", "msg": f"Erro no Guardião: {e}"}), 500

# --- 🆕 ROTA: BUSCAR PERFIL COMPLETO ---
@app.route('/meu_perfil/<email>', methods=['GET'])
def meu_perfil(email):
    try:
        conn = conectar_banco()
        cursor = conn.cursor()
        # Puxa os dados do usuário
        cursor.execute("SELECT nome, email, senha, sigla FROM usuarios WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            conn.close()
            return jsonify({"status": "erro", "msg": "Mestre não encontrado!"}), 404

        nome_usuario = user[0]
        
        # Puxa só as obras desse usuário específico usando o NOME como chave
        cursor.execute("SELECT codigo, data_criacao FROM tesouros WHERE usuario = ?", (nome_usuario,))
        obras = cursor.fetchall()
        conn.close()

        # O Oráculo C++ limpa o código das obras (modo 'd' de descripto)
        lista_obras = [{"codigo": usar_oraculo_cpp(o[0], 'd'), "data": o[1]} for o in obras]

        return jsonify({
            "nome": user[0],
            "email": user[1],
            "senha": user[2], 
            "sigla": user[3],
            "obras": lista_obras
        })
    except Exception as e:
        return jsonify({"status": "erro", "msg": str(e)}), 500

# --- SALVAR E LISTAR TESOUROS (MANTIDOS) ---
@app.route('/salvar_tesouro', methods=['POST'])
def salvar_tesouro():
    dados = request.json
    usuario = dados.get('usuario')
    codigo_puro = dados.get('codigo')
    
    # Chama o Guardião Java para autorizar a forja
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
    print("\n🔥 MOTOR ULTRA LIGADO: PERFIL E CADASTRO ATIVOS 🔥\n")
    app.run(port=5000, debug=True)
