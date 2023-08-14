'''from flask import Flask, request

app=Flask(__name__)
@app.route("/")
def home():
    app.logger.info(f'solicitud en la ruta {request.path}')
    return "<p>Hola mundo bienvenidos a flask</p>"

@app.route("/saludar/<nombre>")
def saludar(nombre):
    app.logger.info(f'solicitud en la ruta {request.path}')
    return f"Hola {nombre}"

@app.route("/edad/<int:edad>")
def edad(edad):
    app.logger.info(f'solicitud en la ruta {request.path}')
    return f"Tu edad es {edad}"

@app.get("/api/user/<user>")
def user(user):
    valores={'user':user}
    return valores'''


from flask import Flask, jsonify, request

app = Flask(__name__)

# Se importa el otro archivo de python que es products.py
from products import products


# http://127.0.0.1:5000/ping cuando se entra a la ruta el servidor respondera "pong!"
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})

# http://127.0.0.1:5000/products El servidor traera el vector products y se mostrara el contenido
@app.route('/products')
def getProducts():
    # return jsonify(products)
    return jsonify({'products': products})


# http://127.0.0.1:5000/products/laptop  traera el nombre del producto dependiendo de lo que se escribe en este caso sera "laptop"
@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productsFound = [
        #hacemos ciclo for, recorre y si encuentra el objeto que coincida retorna el valor de la lista que se puso
        product for product in products if product['name'] == product_name.lower()]
    # con el if hacemos que si el objeto que se escribio esta, lo imprime y si no esta aparece objeto no encontrado
    if (len(productsFound) > 0):
        return jsonify({'product': productsFound[0]})
    return jsonify({'message': 'Product Not found'})

# http://127.0.0.1:5000/products/ es la direccion que se usa para agregar el dato que quiera
@app.route('/products', methods=['POST'])
def addProduct():
    new_product = {
        'name': request.json['name'],
        'price': request.json['price'],
        'quantity': 10
    }
    products.append(new_product)
    return jsonify({'products': products})

# http://127.0.0.1:5000/products/laptop es la direccion que se usa para actualizar y el ultimo "/" se usa para seleccionar el dato que se cambiara
@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if (len(productsFound) > 0):
        productsFound[0]['name'] = request.json['name']
        productsFound[0]['price'] = request.json['price']
        productsFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            'message': 'Product Updated',
            'product': productsFound[0]
        })
    return jsonify({'message': 'Product Not found'})

# http://127.0.0.1:5000/products/laptop es la direccion que se usa para eliminar y el ultimo "/" se usa para seleccionar el dato que se eliminara ya que al no tener id se reemplazara por el nombre del dato
@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productsFound = [product for product in products if product['name'] == product_name]
    if len(productsFound) > 0:
        products.remove(productsFound[0])
        return jsonify({
            'message': 'Product Deleted',
            'products': products
        })

if __name__ == '__main__':
    app.run(debug=True, port=4000)




























