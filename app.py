from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import urllib.request, json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///filmes.sqlite3"
app.secret_key = 'testeteteste'

db = SQLAlchemy(app)

class filmes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30))
    descricao = db.Column(db.String(80))
    ch = db.Column(db.Integer)
    
    def __init__(self, nome, descricao, ch): 
        self.nome = nome
        self.descricao = descricao
        self.ch = ch

avaliacoes = []

@app.route("/")
def home():
    return render_template("menu.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        if request.form.get("nome") and request.form.get("nota"):
            avaliacoes.append({"nome": request.form.get("nome"), "nota": request.form.get("nota")})
    return render_template("cadastro.html", avaliacoes=avaliacoes)

@app.route("/filmes/<propriedade>")
def lista(propriedade):
    
    if propriedade == 'populares':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=c9f8d754d895a1934300c630740ed857"
    elif propriedade == 'kids':
        url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=c9f8d754d895a1934300c630740ed857"
    elif propriedade == '2010':
        url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vote_average.desc&api_key=c9f8d754d895a1934300c630740ed857"
    elif propriedade == 'drama':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=c9f8d754d895a1934300c630740ed857"
    elif propriedade == 'tom_cruise':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=878&with_cast=500&sort_by=vote_average.desc&api_key=c9f8d754d895a1934300c630740ed857"
    
    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
    return render_template("lista.html", filmes=jsondata['results'])

@app.route('/lista-filmes')
def lista_filmes():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    todos_filmes = filmes.query.paginate(page=page, per_page=per_page)
    return render_template("filmes.html", filmes=todos_filmes)

@app.route('/cadastro-filmes', methods=["GET", "POST"])
def cadastro_filmes():
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')
    if request.method == "POST":
        if not nome or not descricao or not ch:
            flash("Preencha todos os campos do formulário", "error")
        else:
            filme = filmes(nome, descricao, ch)
            db.session.add(filme)
            db.session.commit()
            return redirect(url_for('lista_filmes'))
    return render_template("cadastro_filmes.html")

@app.route('/<int:id>/atualiza_filmes', methods=["GET", "POST"])
def atualiza_filmes(id):
    filme = filmes.query.filter_by(id=id).first()
    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        ch = request.form["ch"]
        
        filmes.query.filter_by(id=id).update({"nome": nome, "descricao": descricao, "ch": ch})
        db.session.commit()
        return redirect(url_for('lista_filmes'))
    return render_template("atualizafilme.html", filme=filme)

@app.route('/<int:id>/remove_filmes')
def remove_filmes(id):
    filme = filmes.query.filter_by(id=id).first()
    db.session.delete(filme)
    db.session.commit()
    return redirect(url_for('lista_filmes'))
if __name__ == ("__init__"):
    app(debug=True)