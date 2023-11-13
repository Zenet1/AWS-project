from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('index.html')

def pagina_no_encontrada(error):
    return "Ou", 404

'''
with app.app_context():
    # Acá se pueden inicializar las dbs en memoria
'''

if __name__ == '__main__':
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug = True, port = 5000)
