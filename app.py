# importar framework de FastAPI
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# importar libreria de json para poder utilizar sus archivos
import json

# Schema para validar creacion de productos
from schemas import CreateProduct, UpdateProduct

app = FastAPI()

# agregar configuracion
app.title = 'FastInventory'
app.description = 'REST API para administrar productos'
app.version = '1.0.0'


# Endpoint para mostrar pagina web
@app.get('/')
def home_page():
    html_content = '''
    Welcome to FastAPI
    '''
    return HTMLResponse(html_content)


# Endpoint para obtener productos
@app.get('/products')
def get_products():
    # Obtener los productos desde el archivo JSON
    with open(file='db.json', mode='r', encoding='utf-8') as db:
        # Aqui se encuentran todo el JSON
        data = json.load(db)

    # Extraer productos del JSON
    products = data['products']

    return products


# Endpoint para crear producto
@app.post('/products/create')
def create_product(product: CreateProduct):
    # Obtener los productos desde el archivo JSON
    with open(file='db.json', mode='r', encoding='utf-8') as db:
        # Aqui se encuentran todo el JSON
        data = json.load(db)

    # Extraer productos del JSON
    products = data['products']

    # Validar si el SKU ya existe
    for item in products:

        if item['sku'] == product.sku:
            return 'El SKU ya se encuentra registrado, intenta con otro.'

    # Crear nuevo producto
    new_product = {
        'sku': product.sku,
        'name': product.name,
        'price': product.price
    }

    # Insertar nuevo producto en la lista de productos
    products.append(new_product)

    # Insertar lista de productos actualizada al JSON
    data['products'] = products

    with open(file='db.json', mode='w', encoding='utf-8') as db:
        # Aqui se encuentran todo el JSON
        json.dump(data, db, indent=2)

    return 'Producto registrado con exito'


# Endpoint para actualizar producto
@app.put('/products/update/{sku}')
def update_product(sku: str, product: UpdateProduct):
    # Obtener los productos desde el archivo JSON
    with open(file='db.json', mode='r', encoding='utf-8') as db:
        # Aqui se encuentran todo el JSON
        data = json.load(db)

    # Extraer productos del JSON
    products = data['products']

    # Validar si el SKU ya existe, si existe actualizamos
    for index, item in enumerate(products):

        if item['sku'] == sku:
            
            # Actualizar producto
            item['name'] = product.name
            item['price'] = product.price 

            # Buscamos el producto en la lista por el indice y lo actualimos
            products[index] = item

            # Insertar producto actualizado en el JSON
            data['products'] = products

            with open(file='db.json', mode='w', encoding='utf-8') as db:
                # Actualizamos el JSON
                json.dump(data, db, indent=2)

            return {
                'message': 'Producto actualizado con exito',
                'product': item
            }

    # Este codigo se ejecuta si el for termina y no encuentra un producto por el sku
    return 'El producto no existe'


# Endpoint para eliminar producto
@app.delete('/products/delete/{sku}')
def delete_product(sku: str):
    # Obtener los productos desde el archivo JSON
    with open(file='db.json', mode='r', encoding='utf-8') as db:
        # Aqui se encuentran todo el JSON
        data = json.load(db)

    # Extraer productos del JSON
    products = data['products']

    for index, item in enumerate(products):

        if item['sku'] == sku:
            
            # Eliminar producto mediante el indice
            products.pop(index)

            # Actualizamos la lista de productos (habiendo eliminado uno)
            data['products'] = products

            with open(file='db.json', mode='w', encoding='utf-8') as db:
                # Actualizamos el JSON
                json.dump(data, db, indent=2)

            return f'El producto {sku} ha sido eliminado con exito'
        
    return 'El producto no existe'
