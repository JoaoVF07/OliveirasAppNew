from app import app
from flask import render_template, url_for, request, redirect, flash, session
from app.models import Executar,conexao, cursor, userAtt, setUser, User, MostrarDados, deleteDate, editDate
from datetime import datetime

@app.route('/')
def homepage():
    # Renderiza o template index.html
    return render_template('login.html')

@app.route('/', methods=['POST'])
def login():

    if userAtt:
        dados = MostrarDados()
        return render_template('inicio.html', user=user, dados=dados)
    else:


        email = request.form['email']
        senha = request.form['senha']
        user = User(email,senha)


        dados = MostrarDados()

        comando = f'SELECT * FROM user WHERE email = "{email}" and senha = "{senha}"'
        cursor.execute(comando)
        user = cursor.fetchone()
        
        
        
        if user:

            session['email'] = email  # Armazena o email na sessão
            session['senha'] = senha

            comando = f'SELECT nome FROM user WHERE email = "{email}"'
            cursor.execute(comando)
            nome = cursor.fetchone()[0]
            setUser(True)
            return render_template('inicio.html', nome=nome, dados=dados)

@app.route('/inicio')
def inicio():
     
    email = session.get('email')  # Obtém o email da sessão
    senha = session.get('senha') 

    dados = MostrarDados()

    comando = f'SELECT nome FROM user WHERE email = "{email}"'
    cursor.execute(comando)
    nome = cursor.fetchone()[0]
    return render_template("inicio.html", nome=nome, dados=dados)

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def processar():
    # Recebe os dados do formulário enviado
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    comando = f'INSERT INTO user (nome, email, senha) VALUES ("{nome}","{email}","{senha}")'
    Executar(comando)

   
    setUser(True)
    return redirect(url_for('homepage'))

@app.route('/marcar-data')
def marcData():
    return render_template('marcarData.html')

@app.route('/marcar-data', methods=['POST'])
def post():
    #idUser nosso id do usuario

    email = session.get('email')  # Obtém o email da sessão
    senha = session.get('senha')  # Obtém a senha da sessão

    comando = f'SELECT id FROM user WHERE email = "{email}" and senha = "{senha}"'
    cursor.execute(comando)
    idUser = cursor.fetchone()[0]
    data = request.form['data']
    print("O seu email é ", email)

    comando2 = f'INSERT INTO dataMarc (dataMarcada, userId) VALUES ("{data}",{idUser})'
    connect = Executar(comando2)
    if connect:
        return redirect(url_for('datas'))
    
    return render_template('marcarData.html')
@app.route('/datas')
def datas():
    comando = '''
    SELECT user.nome, dataMarc.dataMarcada 
    FROM dataMarc 
    JOIN user ON dataMarc.userId = user.id
    ORDER BY dataMarc.dataMarcada ASC
    '''
    cursor.execute(comando)
    dados = cursor.fetchall()
    print(dados)
    return render_template("datas.html", dados=dados)

@app.route('/datas', methods=['POST'])
def delete_date():

    email = session.get('email')
    senha = session.get('senha')
    user = request.form['user']
    date = request.form['date']
    comando = f'SELECT nome FROM user WHERE senha = "{senha}" and email = "{email}"'
    cursor.execute(comando)
    userU = cursor.fetchone()[0]

    deleteDate(user,date, userU)
    dados = MostrarDados()
    return render_template("datas.html", dados=dados)

@app.route('/datas', methods=['POST'])
def edit_date_form():
    return render_template("datas.html")

@app.route('/edit_date', methods=['POST','GET'])
def edit_date():
    senha = session.get('senha')
    email = session.get('email')
    user = request.form['user']
    date = request.form['date']
    session['user'] = user
    session['date'] = date
    comando = f'SELECT nome FROM user WHERE senha = "{senha}" and email = "{email}"'
    cursor.execute(comando)
    userU = cursor.fetchone()[0]
    if user != userU:
        return redirect(url_for('datas'))
    return redirect(url_for('edit_page', user=user, date=date))

@app.route('/edit_page', methods=['POST','GET'])
def edit_page():
    # Get form data
    novaData = request.form.get('data')
    user = session.get('user')
    date = session.get('date')
    # Get user credentials from session
    email = session.get('email')
    senha = session.get('senha')

    # Query database to check user credentials
    comando = f'SELECT nome FROM user WHERE senha = "{senha}" and email = "{email}"'
    cursor.execute(comando)
    userU = cursor.fetchone()[0]
    
    # Check if novaData is not None and not empty
    if novaData:
        # Call editDate function
        print("User: ",user,"\nUserU: ",userU)
        ed = editDate(novaData, user, date, userU)
        if ed:  
            return redirect(url_for('datas'))  # Redirect if editDate was successful
        else:
            flash('Failed to edit date!', 'error')  # Flash an error message if editDate failed
    else:
        flash('Invalid data!', 'error')  # Flash an error message if novaData is None or empty
        
    return render_template("editPage.html")  # Render editPage.html