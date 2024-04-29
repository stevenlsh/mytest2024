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

def create_invoices_from_sales_orders():
    # Fetch sales orders that are confirmed but not yet invoiced
    order_ids = models.execute_kw(db, uid, password, 'sale.order', 'search', [[['invoice_status', '=', 'to invoice'], ['state', '=', 'sale']]])

    for order_id in order_ids:
        # Retrieve the date_order and partner_id from the sales order
        order_data = models.execute_kw(db, uid, password, 'sale.order', 'read', [order_id, ['date_order', 'partner_id']])
        if not order_data or 'date_order' not in order_data[0] or 'partner_id' not in order_data[0]:
            print(f"Missing data for sales order {order_id}. Skipping.")
            continue
        date_order = datetime.strptime(order_data[0]['date_order'], '%Y-%m-%d %H:%M:%S')
        
        # Generate a random date within 30 days after the date_order
        random_days = random.randint(0, 30)
        invoice_date = date_order + timedelta(days=random_days)
        invoice_date_str = invoice_date.strftime('%Y-%m-%d')

        # Prepare invoice data
        invoice_vals = {
            'move_type': 'out_invoice',  # 'out_invoice' for customer invoices
            'partner_id': order_data[0]['partner_id'][0],  # Assuming partner_id is stored correctly
            'invoice_date': invoice_date_str,
            'date': invoice_date_str,
            'invoice_line_ids': [(0, 0, {
                'name': 'Product line',
                'quantity': 1,
                'price_unit': 100,  # Placeholder for your product price
                # Add more details depending on your product setup
            })],
        }
        
        # Create the invoice
        invoice_id = models.execute_kw(db, uid, password, 'account.move', 'create', [invoice_vals])

        # Confirm the invoice (post it)
        models.execute_kw(db, uid, password, 'account.move', 'action_post', [invoice_id])
        
        print(f'Created and confirmed invoice {invoice_id} for sales order {order_id} with invoice date {invoice_date_str}')

# Execute the function
create_invoices_from_sales_orders()
