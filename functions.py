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
            nome TEXT NOT NULL,
            telefone TEXT,
            senha TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS compartimentos(
            id_compartimento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_dono INTEGER NOT NULL,
            FOREIGN KEY (id_dono) REFERENCES usuarios(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS remedios(
            id_remedio INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            id_dono INTEGER NOT NULL,
            id_compartimento INTEGER NOT NULL,
            hora1 TEXT,
            hora2 TEXT,
            hora3 TEXT,
            FOREIGN KEY (id_dono) REFERENCES usuarios(id),
            FOREIGN KEY (id_compartimento) REFERENCES compartimentos(id_compartimento)
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

        for _ in range(4):
            cursor.execute('INSERT INTO compartimentos (id_dono) VALUES (?)', (id_dono,))
            conn.commit()

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

def banco_remedio(nomeRemedio, id_dono, id_compartimento, hora1='Não definido', hora2='Não definido', hora3='Não definido'):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    # Verifica se já existe um remédio neste compartimento
    cursor.execute('SELECT COUNT(*) AS total FROM remedios WHERE id_compartimento = ? AND id_dono = ?', (id_compartimento, id_dono))
    total_no_compartimento = cursor.fetchone()['total']
    if total_no_compartimento > 0:
        conn.close()
        return "Este compartimento já contém um remédio"

    # Verifica se o dono já possui 4 remédios no total
    cursor.execute('SELECT COUNT(*) AS total FROM remedios WHERE id_dono = ?', (id_dono,))
    total = cursor.fetchone()['total']
    if total >= 4:
        conn.close()
        return "Limite de 4 remédios por usuário atingido"

    # Insere a bosta do remédio
    cursor.execute('''
        INSERT INTO remedios (nome, id_dono, id_compartimento, hora1, hora2, hora3)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nomeRemedio, id_dono, id_compartimento, hora1, hora2, hora3))

    conn.commit()
    conn.close()
    return True

def deleteRemediosBanco():
    id_dono = session['id_dono']
    conn = sqlite3.connect('database.db')
    
    conn.execute('DELETE FROM remedios WHERE id_dono = ?', (id_dono,))

    session.pop('temHorarios', None)

    conn.commit()
    conn.close()    

def deleteAccountBanco():
    id_dono = session['id_dono']

    conn = sqlite3.connect('database.db')

    conn.execute('DELETE FROM usuarios WHERE id = ?', (id_dono,))
    conn.execute('DELETE FROM compartimentos WHERE id_dono = ?', (id_dono))

    conn.commit()
    conn.close()

def getDataFromBd():
    conn = sqlite3.connect('database.db')
    id_dono = session['id_dono']
    return conn.execute('SELECT FROM remedios WHERE id_dono = ?', id_dono)