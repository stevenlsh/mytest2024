import random
import xmlrpc.client

# Configuration for your Odoo server
url = 'https://my-einvoicing.com'
db = 'test-invoice'
username = 'odoo'
password = 'admin'

# XML-RPC Common and Object endpoints
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def create_random_quotation():
    # Fetch random customer
    customer_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]])
    customer_id = random.choice(customer_ids)

    # Fetch random product
    product_ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[]])
    product_id = random.choice(product_ids)
    product_data = models.execute_kw(db, uid, password, 'product.product', 'read', [product_id, ['list_price']])
    unit_price = product_data[0]['list_price']
    quantity = random.randint(1, 100)

    # Create quotation
    order_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [{
        'partner_id': customer_id,
        'order_line': [(0, 0, {
            'product_id': product_id,
            'product_uom_qty': quantity,
            'price_unit': unit_price,
        })],
    }])

    print(f'Created quotation with customer ID {customer_id}, product ID {product_id}, quantity {quantity}, unit price {unit_price:.2f}')
    return order_id

# Example usage
create_random_quotation()
