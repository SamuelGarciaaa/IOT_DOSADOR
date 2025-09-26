from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__, template_folder='templates')

codes = {}

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
    error = None
    inputTokenTyped = request.form.get('token')

    if inputTokenTyped and inputTokenTyped.strip():
        #Tem algo na variável

        if inputTokenTyped in codes:
            #Código existe

            now = time.time()
            timestamp = codes[inputTokenTyped]
            
            #60 segundos = 1 minuto
            if now - timestamp > 60:
                #Erro, código expirou
                error = 'Erro! Tempo expirado!'
                return render_template('connect.html', error=error)
            
            else:
                #Envia para a página de criação de usuário
                return render_template('login_register.html')

        else:
            #Erro
            error = 'Erro! Código não encontrado!'
            return render_template('connect.html', error=error)

    else:
        #Deu erro
        error = 'Erro! Digite um código válido!'

        return render_template('connect.html', error=error)

@app.route('/login_register')
def login_register():
    pass

@app.route('/')
def index():
    return render_template('connect.html')

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0", port = 5000)