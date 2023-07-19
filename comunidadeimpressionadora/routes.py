from flask import render_template, redirect, url_for, flash, request
from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormResetSenha
from comunidadeimpressionadora.models import Usuario

lista_usuarios = ['Lira', 'João', 'Alon', 'Alessandra', 'Amanda']


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_resetsenha = FormResetSenha()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))
    elif form_resetsenha.validate_on_submit() and 'botao_submit_resetsenha' in request.form:
        # Lógica para redefinir a senha
        flash(f'Senha redefinida com sucesso no e-mail: {form_resetsenha.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_resetsenha=form_resetsenha)


@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    form_criarconta = FormCriarConta()

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        existing_user = Usuario.query.filter_by(email=form_criarconta.email.data).first()
        if existing_user:
            flash('O e-mail já está sendo usado por outro usuário.', 'alert-danger')
            return redirect(url_for('criarconta'))
        usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data,
                          senha=form_criarconta.senha.data)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criarconta.html', form_criarconta=form_criarconta)


@app.route('/resetsenha', methods=['GET', 'POST'])
def resetsenha():
    form_resetsenha = FormResetSenha()

    if form_resetsenha.validate_on_submit() and 'botao_submit_resetsenha' in request.form:
        # Lógica para redefinir a senha
        flash(f'Senha redefinida com sucesso no e-mail: {form_resetsenha.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('resetsenha.html', form_resetsenha=form_resetsenha)
