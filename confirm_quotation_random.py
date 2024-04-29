import random
from datetime import datetime, timedelta
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

def confirm_quotations():
    # Fetch quotations that can be confirmed (filter by state if necessary)
    quotation_ids = models.execute_kw(db, uid, password, 'sale.order', 'search', [[['state', 'in', ['draft', 'sent']]]])
    
    for order_id in quotation_ids:
        # Generate a random date within the last 700 days
        random_days = random.randint(0, 700)
        confirm_date = datetime.now() - timedelta(days=random_days)
        confirm_date_str = confirm_date.strftime('%Y-%m-%d %H:%M:%S')

        # Update the date_order to the randomly generated date
        models.execute_kw(db, uid, password, 'sale.order', 'write', [order_id, {
            'date_order': confirm_date_str
        }])

        # Confirm the quotation
        models.execute_kw(db, uid, password, 'sale.order', 'action_confirm', [order_id])
        print(f'Confirmed quotation {order_id} with date {confirm_date_str}')

# Execute the function
confirm_quotations()
