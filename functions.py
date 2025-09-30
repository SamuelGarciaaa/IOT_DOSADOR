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

    #Se sobrar tempo, colocar quantidade

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS remedios(
            id_remedio INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            id_dono INTEGER NOT NULL,
            hora1 TEXT,
            hora2 TEXT,
            hora3 TEXT,
            
            FOREIGN KEY (id_dono) REFERENCES usuarios(id)
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
        cursor.execute('SELECT * FROM usuarios WHERE nome = ? AND senha = ?', (nome, senha))

        if cursor.fetchone():
            conn.close()
            return True
        
        else:
            return False