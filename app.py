from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from funcoes import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/carros_e_clientes'
db = SQLAlchemy(app)
app.secret_key = 'fabricio'

class Carros(db.Model):
    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True) 
    nome = db.Column(db.String(60))
    modelo = db.Column(db.String(60))
    preco = db.Column(db.Float)
    registro = db.Column(db.Date())   
    combustivel = db.Column(db.Enum("gasolina","etanol","diesel","biodiesel","GNV","eletricidade","hibrido","flex"))
    motor = db.Column(db.String(20))
    transmissao = db.Column(db.Enum('automática','manual','automatizada')) 
    origem = db.Column(db.String(40))
    Co2 = db.Column(db.Integer)
    estado = db.Column(db.Enum('usado','novo')) 
    quilometros = db.Column(db.Integer)
    garantia = db.Column(db.String(40))
    tipo = db.Column(db.String(30))
    portas = db.Column(db.Integer)
    cor = db.Column(db.String(30))
    lugares = db.Column(db.Integer)

class Clientes(db.Model):
    id = db.Column('id',db.Integer, primary_key=True, autoincrement=True)  
    nome  = db.Column(db.String(50))
    numero = db.Column(db.String(20))
    email = db.Column(db.String(100))
    senha = db.Column(db.String(64))
    administrador = db.Column(db.Integer)



nome_carro_da_semana = 'Kia Sorento'


@app.route('/')
def home():
    #esta data_preco ajusta a data e os valores para o padrão brasileiro
    carro_da_semana = data_preco(Carros.query.filter_by(nome=nome_carro_da_semana).first())
    img_carro_da_semana = str(carro_da_semana.nome).replace(' ','-')
    return render_template('home.html',carro_da_semana=carro_da_semana, img_carro_da_semana=img_carro_da_semana,nome_carro_da_semana=nome_carro_da_semana)



@app.route('/logar',methods=['POST'])
def processar_login():
    c = 0
    data = request.form
    email_usuario = data.get('email_login')
    senha_usuario = data.get('senha_login')
    usuarios = Clientes.query.all()

    for usuario in usuarios:
        if email_usuario == usuario.email:
            c += 1
        if senha_usuario == usuario.senha:
            c += 1
    print(c)
    if c == 3:
        return redirect(url_for('carros'))
    else:
        return redirect(url_for('home'))


@app.route('/sobre nós')
def sobre():
    return render_template('sobre.html')

@app.route('/layout')
def lay():
    return render_template('layout.html')





@app.route('/carros')
def carros():
    lst_marcas_carros = []
    lst_marcas = []
    anos = list(range(1956, 2025))
    carros = data_preco(Carros.query.all())
    for carro in carros:
        marca_carro = str(carro.nome.split()[0]) # pega somente a marca do carro
        if marca_carro not in lst_marcas: #adiciona marcas de carros sem repetição
            lst_marcas.append(marca_carro)


        marca_nome_carro = str(carro.nome).replace(' ','-') #tira espaços do no nome do carro
        lst_marcas_carros.append(marca_nome_carro)
    return render_template('carros.html',carros=carros,lst_marcas=lst_marcas,lst_marcas_carros=lst_marcas_carros,anos=anos)

@app.route('/processamento',methods=['POST'])
def processar():
    data = request.form
    query_dict = {}
    lst_marcas = []
    carros = Carros.query.all()
    query_dict['registro'] = [int(data.get('select_registro_inicio')),int(data.get('select_registro_fim'))]
    query_dict['preco'] = [float(data.get('select_preco_inicio')),float(data.get('select_preco_fim'))]
    query_dict['quilometro'] = [int(data.get('select_quilometro_inicio')),int(data.get('select_quilometro_fim'))]
    if len(data.getlist('combustivel')) > 0:
        query_dict['combustivel'] = data.getlist('combustivel')
    else:
         query_dict['combustivel'] = ["gasolina","etanol","diesel","biodiesel","GNV","eletricidade","hibrido","flex"]
    if data.get('estado') == None:
        query_dict['estado'] = ['novo','usado']
    else:
        query_dict['estado'] = data.get('estado')


    for carro in carros:
        marca_carro = str(carro.nome.split()[0])
        if marca_carro not in lst_marcas: 
            lst_marcas.append(marca_carro)
        if len(data.getlist('marcas')) == 0:
            query_dict['marcas'] = lst_marcas
        else:
             query_dict['marcas'] =  data.getlist('marcas')
        if query_dict['registro'][0] <= carro.registro.year <= query_dict['registro'][1]:
            if query_dict['preco'][0] <= carro.preco <= query_dict['preco'][1]:
                if query_dict['quilometro'][0] <= carro.quilometros <= query_dict['quilometro'][1]:
                    print(f"""Marcas escolhidas:{query_dict['marcas']} - nome e marca: {carro.nome}
Registro:{query_dict['registro'][0]} <= {carro.registro.year} <= {query_dict['registro'][1]}
Preço:{query_dict['preco'][0]} <= {carro.preco} <= {query_dict['preco'][1]}
Quilometragem:{query_dict['quilometro'][0]} <= {carro.quilometros} <= {query_dict['quilometro'][1]}
Combustíveis escolhidos:{query_dict['combustivel']} - combustível:{carro.combustivel}
Estados escolhidos:{query_dict['estado']} - estado:{carro.estado}\n""")
                    
    return redirect(url_for('carros'))

@app.route('/carros/<string:carro_nome>',methods=['POST','GET'])
def carro_especifico(carro_nome):
    carro = Carros.query.filter_by(nome=carro_nome).first()
    marca_nome_carro = str(carro.nome).replace(' ','-')
    marca_carro = str(carro.nome).split()[0]
    carro.preco = moedinha(carro.preco)
    carro.registro = carro.registro.strftime('%d/%m/%Y')
    return render_template('carro_especifico.html',carro=carro,marca_nome_carro=marca_nome_carro,marca_carro=marca_carro)

@app.route('/contatos')
def contatos():
    return render_template('contatos.html')

@app.route('/email_processar',methods=['POST'])
def processar_email():
    selecao = request.form.get('email_selecao')
    titulo = request.form.get('email_titulo')
    remetente = request.form.get('email_remetente')
    corpo = request.form.get('email_corpo')
    enviar_email(assunto=f'-{selecao}- {titulo}',texto=corpo,remetente='testeconsilcar@gmail.com',destinatário='testeconsilcar@gmail.com')
    return redirect(url_for('contatos'))


