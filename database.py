from flask_sqlalchemy import SQLAlchemy

# Armazenando o sqlalchemy dentro da variável DB
db = SQLAlchemy()

# Criando um modelo (tabela) do sqlalchemy que será responsável por armazenar os
# EXERÍCIOS EXISTENTES no sistema
class Exercicio(db.Model):
    __tablename__ = 'Exercicio'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

# Criando um modelo (tabela) do sqlalchemy que será responsável por
# armazenar dados da classe Exercício (ForeignKey), porém com o Extra de Séries e Carga kg
# Para que seja exibida na página inicial como o treino do dia.
class TreinoDia(db.Model):
    __tablename__ = 'TreinoDia'

    # O id do exercício é uma 
    id = db.Column(db.Integer, primary_key=True)

    # Nome recebe o id do exercicio na tabela pai (Exercicio) como foreigner key
    name = db.Column(
        db.Integer,
        db.ForeignKey('Exercicio.id'),
        nullable=False
        )
        
    
    series = db.Column(db.Integer, nullable=False)
    carga = db.Column(db.Integer, nullable=False)

    # Relacionamento ORM com a tabela Exercicio (acesso aos dados do exercício)
    exercicio = db.relationship('Exercicio')

# Efetiva criação do banco
#def criar_banco():
#    with app.app_context():
#        db.create_all()
#criar_banco()