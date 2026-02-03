import sqlite3

def inicializar_reino():
    # Cria o arquivo do banco de dados (o nosso cofre)
    conn = sqlite3.connect('reino_celeste.db')
    cursor = conn.cursor()

    print("⚒️ Construindo as fundações do Reino...")

    # Tabela de Usuários (Pra saber quem é Criador Real)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE,
            sigla TEXT DEFAULT '[CD-👑]'
        )
    ''')

    # Tabela de Tesouros (Onde os códigos da Forja vão morar)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tesouros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            codigo TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Tabela de Livros (Para os seus 76 capítulos!)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capitulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro TEXT DEFAULT 'Celeste Dragon',
            numero INTEGER,
            titulo TEXT,
            conteudo TEXT
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Cofre Real construído com sucesso! O SQL está pronto.")

if __name__ == "__main__":
    inicializar_reino()
