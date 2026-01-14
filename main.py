from flask import Flask, render_template, request, redirect
from database import db, Exercicio, TreinoDia

# Aqui é onde vão ficar as rotas!

# Configurando o DATABASE!
app = Flask(__name__)
# DEFINE A URI DO BANCO DE DADOS SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///exercicios.db'
db.init_app(app)

# Tela inicial/Exibição dos treinos do dia
@app.route('/')
def main():
    # Treino_Dia é referente a tudo o que está na tabela TreinoDia no database
    treino_dia = TreinoDia.query.all()
    # Retorna o template e marca que treinodia é igual a variável Treino_Dia
    return render_template('main.html', treinos=treino_dia)

# Função que DELETA TODOS OS EXERCICIOS em TreinoDia caso todos estejam marcados na checklist front
@app.route('/concluir-treino', methods=['POST'])
def concluir_treino():
    TreinoDia.query.delete()
    db.session.commit()
    return redirect('/')

'''
FUNÇÃO QUE POSSIBILITA A EXCLUSÃO DE EXERCÍCIOS DISPONÍVEIS NA PARTE
DE CRIAR EXERCÍCIOS
'''
@app.route('/deletar-exercicio', methods=['POST'])
def deletar_exercicio():
    exercicios_pra_deletar = request.form.getlist('ex_id')
    
    if exercicios_pra_deletar:

        # Converte a lista de strings para inteiros
        exercicios_para_deletar = [int(id) for id in exercicios_pra_deletar]

        # Executa o delete filtrado
        # 'Delete da tabela Exercicio onde o ID estiver em exercicios_para_deletar'
        Exercicio.query.filter(Exercicio.id.in_(exercicios_para_deletar)).delete(synchronize_session=False)

        # Salva a alteração
        db.session.commit()

    return redirect('/criar-exercicio')

# Lista de exercícios DISPONÍVEIS PARA USAR EM TREINOS DO DIA!
@app.route('/listar-exercicios', methods=['GET', 'POST'])
def listar_exercicios():
   # exercicio é referente a tudo o que está na tabela Exercicio no database
   exercicio = Exercicio.query.all()

    # Caso o metodo seja post
   if request.method == 'POST':
       
        # O request.form.getlist('exercicios') é usado quando se tem multiplos elementos no html
        # com o mesmo atributo nome e quer receber todos os valores selecionados DE UMA VEZ SÓ!   
       exercicios_ids = request.form.getlist('ex_id')

        # Para cada exercicio em exercicios ele faz um request no formulario da página listar_exercicios
        # pegando as séries relacionadas com o exercicio em questão e a carga também.
        # após isso, tudo é condensado numa variável chamada 'treino', que é a variável que será "exportada"
        # para a tabela TreinoDia
       for ex_id in exercicios_ids:
           
           series = request.form[f'series_{ex_id}']
           carga = request.form[f'carga_{ex_id}']

           # exercicio_id é = ex_id (definido após o for), series = series (formulario) e carga = carga (formulario)
           treino = TreinoDia(
               
               name=ex_id,
               series=series,
               carga=carga
           )
           db.session.add(treino)  
       db.session.commit()     
       return redirect('/')

   # Retorna o templaye e marca que exercicio é igual a variável exercicio
   return render_template('listar_exercicios.html', exercicios=exercicio)

@app.route('/criar-exercicio', methods=['GET', 'POST'])
def criar_exercicio():
    exercicio = Exercicio.query.all()

    # Caso o metodo seja post 
    if request.method == 'POST':
        name = request.form.get('name')
        novo = Exercicio(name=name)
        db.session.add(novo)
        db.session.commit()
        return redirect('/criar-exercicio')

    return render_template('criar_exercicio.html', exercicio=exercicio)

# Roda o app em modo debug, padrão
if __name__ == '__main__':
    app.run(debug=True)