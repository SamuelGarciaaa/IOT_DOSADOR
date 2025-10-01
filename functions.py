import sqlite3
from flask import session

def banco(nome, senha, metodo, tel=None):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            telefone TEXT,
            senha TEXT NOT NULL
        )
    ''')

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
        # Verifica se já existe
        cursor.execute('SELECT id FROM usuarios WHERE nome = ?', (nome,))
        if cursor.fetchone():
            conn.close()
            return False  # Usuário já existe

        # Se não existir → cadastra
        cursor.execute(
            'INSERT INTO usuarios(nome, telefone, senha) VALUES (?, ?, ?)',
            (nome, tel, senha)
        )
        conn.commit()

        # Pega o id recém-criado
        id_dono = cursor.lastrowid
        session['id_dono'] = id_dono

        conn.close()
        return True

    elif metodo == 'login':
        cursor.execute(
            'SELECT id FROM usuarios WHERE nome = ? AND senha = ?',
            (nome, senha)
        )
        row = cursor.fetchone()

        if row:
            id_dono = row['id']
            session['id_dono'] = id_dono
            conn.close()
            return True
        else:
            conn.close()
            return False


def banco_remedio(nomeRemedio, id_dono, hora1='Não definido', hora2='Não definido', hora3='Não definido'):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Verifica se já existe para este dono
    cursor.execute('SELECT 1 FROM remedios WHERE nome = ? AND id_dono = ?', (nomeRemedio, id_dono))
    if cursor.fetchone():
        conn.close()
        return False # Remédio já existe para este usuário

    cursor.execute('''
        INSERT INTO remedios(nome, id_dono, hora1, hora2, hora3)
        VALUES (?, ?, ?, ?, ?)
    ''', (nomeRemedio, id_dono, hora1, hora2, hora3))

    conn.commit()
    conn.close()
    return True
