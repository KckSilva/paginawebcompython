from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'
app.secret_key = 'supersecretkey'  # Necessário para usar flash
db = SQLAlchemy(app)

# Definição do modelo do banco de dados
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    bio = db.Column(db.Text)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        age = request.form['age']
        bio = request.form['bio']
        
        # Verifica se a idade é um número válido
        try:
            age = int(age)
        except ValueError:
            flash('Idade inválida. Por favor, insira um número.', 'error')
            return redirect('/')
        
        new_user = User(username=username, email=email, age=age, bio=bio)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Dados enviados com sucesso!', 'success')
        except IntegrityError:
            db.session.rollback()  # Reverte a transação para o estado anterior
            flash('Usuário já existe. Por favor, escolha outro nome de usuário.', 'error')
        except Exception as e:
            db.session.rollback()  # Reverte a transação para o estado anterior
            flash(f'Erro ao salvar os dados: {e}', 'error')
        return redirect('/')
    
    return render_template('form.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
