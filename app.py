from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'clave-secreta'

productos = [
    {'id': 1, 'nombre': 'Producto A', 'precio': 100},
    {'id': 2, 'nombre': 'Producto B', 'precio': 150},
    {'id': 3, 'nombre': 'Producto C', 'precio': 200},
]

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/agregar/<int:producto_id>')
def agregar(producto_id):
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        if 'carrito' not in session:
            session['carrito'] = []
        session['carrito'].append(producto)
        session.modified = True

        # Guardar en archivo
        with open('carrito.txt', 'a', encoding='utf-8') as archivo:
            archivo.write(f"{datetime.now()} - {producto['nombre']} - ${producto['precio']}\n")

    return redirect(url_for('carrito'))

@app.route('/carrito')
def carrito():
    carrito = session.get('carrito', [])
    total = sum(p['precio'] for p in carrito)
    return render_template('carrito.html', carrito=carrito, total=total)

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nombre = request.form['nombre']
    return f"<h2>¡Hola, {nombre}! Gracias por contactarte.</h2>"

# ✅ CONFIGURACIÓN CORRECTA PARA RENDER
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
