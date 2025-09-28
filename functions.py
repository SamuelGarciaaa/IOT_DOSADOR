import sqlite3

def banco(nome, senha, metodo, tel=None):
    conn = sqlite3.connect('database.db')
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            senha TEXT NOT NULL
        )
    ''')

    if metodo == 'cadastro':
        #Verifica se já existe
        cursor.execute('SELECT * FROM usuarios WHERE nome = ?', (nome,))
        if cursor.fetchone():
            conn.close()
            return False  #Usuário já existe

        #Se não existir
        cursor.execute('''
            INSERT INTO usuarios(nome, telefone, senha) VALUES (?, ?, ?)
        ''', (nome, tel, senha))

        conn.commit()
        conn.close()

        return True

    elif metodo == 'login':
        pass