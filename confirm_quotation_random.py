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

def confirm_and_update_quotations():
    quotation_ids = models.execute_kw(db, uid, password, 'sale.order', 'search', [[['state', 'in', ['draft', 'sent']]]])
    for order_id in quotation_ids:
        try:
            # Attempt to confirm the quotation
            models.execute_kw(db, uid, password, 'sale.order', 'action_confirm', [order_id])

            # Generate a random date within the last 365 days
            random_days = random.randint(0, 365)
            new_date_order = datetime.now() - timedelta(days=random_days)
            new_date_order_str = new_date_order.strftime('%Y-%m-%d %H:%M:%S')

            # Update the date_order to the randomly generated date after confirming
            models.execute_kw(db, uid, password, 'sale.order', 'write', [order_id, {
                'date_order': new_date_order_str
            }])
            print(f'Confirmed and updated quotation {order_id} with new date {new_date_order_str}')
        
        except xmlrpc.client.Fault as e:
            print(f"Failed to confirm quotation {order_id}: {str(e)}")
            # Additional logic to handle specific errors can be added here.

# Execute the function
confirm_and_update_quotations()
