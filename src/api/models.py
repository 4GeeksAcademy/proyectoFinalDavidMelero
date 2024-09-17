from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String(), nullable=True)
    last_name = db.Column(db.String(), nullable=True)
    is_admin = db.Column(db.Boolean(), default=False)

    # Relaciones con carritos y órdenes
    carts = db.relationship('Carts', backref='user', uselist=False)
    orders = db.relationship('Orders', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'
        
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'is_admin': self.is_admin
        }

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    price = db.Column(db.Integer(), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    image_url = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'
        
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'stock': self.stock,
            'image_url': self.image_url
        }

class CartItems(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    # Relación con productos y carrito
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Products')

    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))
    cart = db.relationship('Carts', backref='cart_items')

    def __repr__(self):
        return f'<CartItem {self.product_id}>'

    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.product.price,  # Precio del producto
            'cart_id': self.cart_id
        }

class Carts(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # Relación con el usuario
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)

    def __repr__(self):
        return f'<Cart {self.id}>'

    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.cart_items)
        
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_price': self.total_price()
        }

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), nullable=False)
    total_price = db.Column(db.Integer(), nullable=False)

    # Relación con el usuario
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relación con los productos en la orden
    order_items = db.relationship('OrderItems', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id}>'
        
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date,
            'total_price': self.total_price
        }

class OrderItems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer(), nullable=False)
    price = db.Column(db.Integer(), nullable=False)

    # Relación con la orden y el producto
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    product = db.relationship('Products')
    order = db.relationship('Orders')

    def __repr__(self):
        return f'<OrderItem {self.id}>'
        
    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price
        }
