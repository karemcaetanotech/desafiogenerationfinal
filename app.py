from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State

# Configuração da aplicação Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Conexão com o banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo do banco de dados para os estudantes
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    nome_professor = db.Column(db.String(100), nullable=False)
    numero_sala = db.Column(db.Integer, nullable=False)

# Configuração da aplicação Dash
app_dash = dash.Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout da aplicação Dash
app_dash.layout = dbc.Container([
    html.H1("Cadastro de Estudantes"),
    dbc.Form([
        dbc.Row([
            dbc.Col(dbc.Label("Nome")),
            dbc.Col(dbc.Input(id='input-nome', placeholder='Digite o nome', type='text')),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Idade")),
            dbc.Col(dbc.Input(id='input-idade', placeholder='Digite a idade', type='number')),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Nota do Primeiro Semestre")),
            dbc.Col(dbc.Input(id='input-nota-1', placeholder='Digite a nota', type='number')),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Nota do Segundo Semestre")),
            dbc.Col(dbc.Input(id='input-nota-2', placeholder='Digite a nota', type='number')),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Nome do Professor")),
            dbc.Col(dbc.Input(id='input-professor', placeholder='Digite o nome do professor', type='text')),
        ]),
        dbc.Row([
            dbc.Col(dbc.Label("Número da Sala")),
            dbc.Col(dbc.Input(id='input-sala', placeholder='Digite o número da sala', type='number')),
        ]),
        dbc.Row([
            dbc.Col(dbc.Button("Salvar", id='btn-save', color='primary')),
        ]),
    ]),
    html.Div(id='output-message')
])

# Callback para salvar os dados no banco de dados
@app_dash.callback(
    Output('output-message', 'children'),
    [Input('btn-save', 'n_clicks')],
    [State('input-nome', 'value'),
     State('input-idade', 'value'),
     State('input-nota-1', 'value'),
     State('input-nota-2', 'value'),
     State('input-professor', 'value'),
     State('input-sala', 'value')]
)
def save_student(n_clicks, nome, idade, nota1, nota2, professor, sala):
    if n_clicks:
        if None in [nome, idade, nota1, nota2, professor, sala]:
            return "Todos os campos devem ser preenchidos."
        
        new_student = Student(
            nome=nome,
            idade=idade,
            nota_primeiro_semestre=nota1,
            nota_segundo_semestre=nota2,
            nome_professor=professor,
            numero_sala=sala
        )
        db.session.add(new_student)
        db.session.commit()
        return f"Estudante {nome} salvo com sucesso!"
    return ""

# Verifica se o script está sendo executado diretamente
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Criação do banco de dados no contexto da aplicação
    app.run(debug=True)
# Código anterior para configurar Flask, Dash, e o banco de dados

if __name__ == '__main__':
    app.run(debug=True, port=3306)
    
from flask_cors import CORS # type: ignore

CORS(app)

