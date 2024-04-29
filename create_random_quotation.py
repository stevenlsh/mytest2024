import random
from faker import Faker
import xmlrpc.client

# Initialize Faker to generate random data
fake = Faker()

# Configuration for your Odoo server
url = 'https://my-einvoicing.com'
db = 'test-invoice'  # Updated with your database name
username = 'odoo'    # Updated with your username
password = 'admin'   # Updated with your password

# XML-RPC Common and Object endpoints
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def create_random_quotation():
    # Generate random data
    customer_name = fake.name()
    product_name = fake.word()
    quantity = random.randint(1, 100)
    unit_price = random.uniform(10.0, 100.0)

    # Create customer
    customer_id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
        'name': customer_name,
        'is_company': False,
        'customer_rank': 1,
    }])

    # Create product
    product_id = models.execute_kw(db, uid, password, 'product.product', 'create', [{
        'name': product_name,
        'type': 'product',
        'list_price': unit_price,
    }])

    # Create quotation
    order_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [{
        'partner_id': customer_id,
        'order_line': [(0, 0, {
            'product_id': product_id,
            'product_uom_qty': quantity,
            'price_unit': unit_price,
        })],
    }])

    print(f'Created quotation for {customer_name} with product {product_name}, quantity {quantity}, unit price {unit_price:.2f}')
    return order_id

# Example usage
create_random_quotation()
