from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

# Error handlers

def pagina_no_encontrada(error):
    return "Ou", 404

def metodo_invalido(error):
    return "Ou invalido", 405

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(405, metodo_invalido)
    app.run(host = '0.0.0.0', debug = True, port = 5000)
