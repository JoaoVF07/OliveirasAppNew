import pymysql
from flask import flash

userAtt = False

conexao = pymysql.connect(
        host='localhost',
        user='root',
        password='Tartaruga20',
        database='area_db',
    )
cursor = conexao.cursor()

def Executar(comando):
    cursor.execute(comando)
    conexao.commit() 
    return True # edita o banco de dados

def setUser(valor):
    userAtt = valor

class User():
    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

arrayUser = []

def MostrarDados():
    comando = '''
        SELECT user.nome, dataMarc.dataMarcada 
        FROM dataMarc 
        JOIN user ON dataMarc.userId = user.id
        ORDER BY dataMarc.dataMarcada ASC LIMIT 5
        '''
    cursor.execute(comando)
    dados = cursor.fetchall()
    return dados

def deleteDate(user, date, userU):
    if userU == user:
        comando = f'DELETE FROM dataMarc WHERE userId = (SELECT id FROM user WHERE nome = "{user}") AND dataMarcada = "{date}"'
        cursor.execute(comando)
        conexao.commit()
    else:
        flash('Voce só pode editar datas suas!', 'error')
# 'UPDATE dataMarc set dataMarcada = "{newdata}" where dataMarcada = "{date}" limit 1'
def editDate(newdata,user, date, userU):
    if userU == user:
        comando = f'UPDATE dataMarc set dataMarcada = "{newdata}" where dataMarcada = "{date}" limit 1'
        cursor.execute(comando)
        conexao.commit()
        print("CHEGOU AQUI")
        return True
    else:
        flash('Voce só pode editar datas suas!', 'error')