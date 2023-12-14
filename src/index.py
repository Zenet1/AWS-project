from app import app
from flask import render_template
from utils.db import ConexionDB
    
@app.route('/')
def index():
    return render_template('index.html')

# Error handlers

def pagina_no_encontrada(error):
    return "ERROR: Página no encontrada", 404

def metodo_invalido(error):
    return "ERROR: Método inválido", 405

with app.app_context():
        ConexionDB.create_all()    

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(405, metodo_invalido)
    
    app.run(debug = True, port = 5000)
