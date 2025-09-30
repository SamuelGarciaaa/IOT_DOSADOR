from flask import render_template, request, jsonify, redirect, url_for, session
import time

from app import app
from functions import *

#Dicionário pra guardar os códigos
codes = {}

#Gambiarra para usar sem o esp32
codes = {'oi' : time.time()}

@app.route('/data', methods=['POST'])
def api():
    try:
        data = request.get_json()
        code = data.get('code')

        if not code:
            #Retorna um erro ao Esp32
            return jsonify({'status': 'error', 'message': 'Nenhum código enviado'}), 400
        
        codes[code] = time.time()
        #Guarda o código e o momento em que ele foi criado
        print(f'Código registrado: {code}')

        #Retorna uma mensagem de sucesso ao Esp32
        return jsonify({'status': 'success', 'message': 'Código registrado'}), 201

    except Exception as e:
        print(e)

@app.route('/inputCode', methods=['POST'])
def inputToken():
    if request.method == 'POST':
        #Erro
        error = None

        #Variável do input
        inputTokenTyped = request.form.get('token')

        if inputTokenTyped and inputTokenTyped.strip():
            #Tem algo na variável

            if inputTokenTyped in codes:
                #Código existe

                now = time.time()
                timestamp = codes[inputTokenTyped]
                
                #120 segundos = 2 minutos
                if now - timestamp > 120:
                    #Erro, código expirou
                    error = 'Erro! Tempo expirado!'
                    return render_template('connect.html', error=error)
                
                else:
                    #Envia para a página de criação de usuário
                    session['pareado'] = True
                    return render_template('login_register.html')

            else:
                #Erro
                error = 'Erro! Código não encontrado!'
                return render_template('connect.html', error=error)

        else:
            #Deu erro
            error = 'Erro! Digite um código válido!'

            return render_template('connect.html', error=error)

@app.route('/login_register', methods=['POST'])
def login_register():
    if request.method == 'POST':
        #Erro
        error = None

        #Variáveis
        variavelQueDizOqueEstamosUsando = request.form.get('variableToTellWhatWeAreUsing')

        nome = request.form.get('nome')
        senha = request.form.get('senha')

        if variavelQueDizOqueEstamosUsando == 'register':
            #Opção registrar
            tel = request.form.get('tel')
            
            if tel and tel.strip() and nome and nome.strip() and senha and senha.strip():
                #Preencheu tudo

                deuCerto = banco(nome, senha, 'cadastro', tel)

                if deuCerto == True:
                    #User area = Área do usuário com os horários e coisas para editar
                    session['nome'] = nome
                    return render_template('userArea.html')
                
                elif deuCerto == False:
                    error = 'Já existe um usuário com esse nome!'
                    return render_template('login_register.html', error=error)

                else:
                    error = 'Algo deu errado! Tente novamente.'
                    return render_template('login_register.html', error=error)

            else:
                error = 'Por favor, preencha todos os campos!'
                return render_template('login_register.html', error=error)

        else:
            #Opção logar
            if nome and nome.strip() and senha and senha.strip():
                #Preencheu tudo

                deuCerto = banco(nome, senha, 'login')

                if deuCerto == True:
                    #User area = Área do usuário com os horários e coisas para editar
                    session['nome'] = nome
                    return render_template('userArea.html')
                
                else:
                    error = 'Erro! Usuário ou senha incorretos!'
                    return render_template('login_register.html', error=error)

            else:
                error = 'Por favor, preencha todos os campos!'
                return render_template('login_register.html', error=error)

@app.route('/remedios', methods=['POST'])
def remedios():
    if request.method == 'POST':
        pass

@app.route('/logout', methods=['POST'])
def logout():
    pass

@app.route('/deleteAccount', methods=["POST"])
def deleteAccount():
    pass

@app.route('/')
def index():
    #Já conectou a maleta
    if session.get('pareado') is True:
        if session.get('nome'):
            return render_template('userArea.html')

        return render_template('login_register.html')
        
    #Não conectou a maleta ainda
    else:
        return render_template('connect.html')