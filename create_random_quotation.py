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

def get_random_product():
    # Fetch random product
    product_ids = models.execute_kw(db, uid, password, 'product.product', 'search', [[]])
    if not product_ids:
        return None, None
    product_id = random.choice(product_ids)
    product_data = models.execute_kw(db, uid, password, 'product.product', 'read', [product_id, ['list_price']])
    unit_price = product_data[0]['list_price']
    return product_id, unit_price

def create_random_quotation():
    # Fetch random customer
    customer_ids = models.execute_kw(db, uid, password, 'res.partner', 'search', [[]])
    if not customer_ids:
        print("No customers found in the database.")
        return
    customer_id = random.choice(customer_ids)

    # Create quotation with 10 random product lines
    order_lines = []
    for _ in range(10):
        product_id, unit_price = get_random_product()
        if not product_id:
            print("No products found in the database.")
            return
        quantity = random.randint(1, 10)  # Random quantity between 1 and 10
        order_lines.append((0, 0, {
            'product_id': product_id,
            'product_uom_qty': quantity,
            'price_unit': unit_price,
        }))

    # Create quotation
    order_id = models.execute_kw(db, uid, password, 'sale.order', 'create', [{
        'partner_id': customer_id,
        'order_line': order_lines
    }])

    print(f'Created quotation with customer ID {customer_id} and 10 product lines.')
    return order_id

# Example usage
create_random_quotation()
