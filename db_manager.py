import sqlite3
import os

def inicializar_reino():
    # Remove o banco antigo para não dar conflito de colunas
    if os.path.exists('reino_celeste.db'):
        os.remove('reino_celeste.db')
        print("🗑️ Resetando banco antigo...")

    conn = sqlite3.connect('reino_celeste.db')
    cursor = conn.cursor()

    print("⚒️ Construindo as fundações reais...")

    # Tabela de Usuários (Agora com SENHA!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            sigla TEXT DEFAULT '[Explorador-🛡️]'
        )
    ''')

    # Tabela de Tesouros
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tesouros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            codigo TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Cofre Real reconstruído com SENHA inclusa!")

if __name__ == "__main__":
    inicializar_reino()
