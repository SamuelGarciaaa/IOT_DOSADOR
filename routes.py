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
        id_dono = session['id_dono']
        erros = []
        sucesso = False

        # Compartimento 1
        if request.form.get('ativar1') == 'yes':
            nome = request.form.get('nome_remedio1')
            h1 = request.form.get('remedio1hora1')
            h2 = request.form.get('remedio1hora2')
            h3 = request.form.get('remedio1hora3')
            deu_certo = banco_remedio(nome, id_dono, 1, h1, h2, h3)

            if deu_certo == True:
                sucesso = True

            else:
                erros.append(f"Compartimento 1: {deu_certo}")

        # Compartimento 2
        if request.form.get('ativar2') == 'yes':
            nome = request.form.get('nome_remedio2')
            h1 = request.form.get('remedio2hora1')
            h2 = request.form.get('remedio2hora2')
            h3 = request.form.get('remedio2hora3')
            deu_certo = banco_remedio(nome, id_dono, 2, h1, h2, h3)

            if deu_certo == True:
                sucesso = True

            else:
                erros.append(f"Compartimento 2: {deu_certo}")

        # Compartimento 3
        if request.form.get('ativar3') == 'yes':
            nome = request.form.get('nome_remedio3')
            h1 = request.form.get('remedio3hora1')
            h2 = request.form.get('remedio3hora2')
            h3 = request.form.get('remedio3hora3')
            deu_certo = banco_remedio(nome, id_dono, 3, h1, h2, h3)

            if deu_certo == True:
                sucesso = True

            else:
                erros.append(f"Compartimento 3: {deu_certo}")

        # Compartimento 4
        if request.form.get('ativar4') == 'yes':
            nome = request.form.get('nome_remedio4')
            h1 = request.form.get('remedio4hora1')
            h2 = request.form.get('remedio4hora2')
            h3 = request.form.get('remedio4hora3')
            deu_certo = banco_remedio(nome, id_dono, 4, h1, h2, h3)

            if deu_certo == True:
                sucesso = True

            else:
                erros.append(f"Compartimento 4: {deu_certo}")

        if sucesso:
            session['temHorarios'] = True

        if erros:
            return render_template('userArea.html', error='<br>'.join(erros))
        
        else:
            return render_template('userArea.html', success="Remédios cadastrados com sucesso!")

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template('connect.html')

@app.route('/deleteRemedios', methods=['POST'])
def deleteRemedios():
    deuCerto = deleteRemediosBanco()

    if deuCerto == True:
        pass

    else:
        return render_template('userArea.html', error='')

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