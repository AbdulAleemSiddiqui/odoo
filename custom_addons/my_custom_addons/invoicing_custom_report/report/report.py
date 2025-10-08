from unittest import result
from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.invoicing_custom_report.invoicing_custom_report_template"
    _description = "Invoicing Custom Report"

    def _get_report_values(self, docids, data=None):
        
        print("I am here in invoicing report")
        print(data.get('from_date'))
        print(data.get('to_date'))


        from_date = data.get('from_date')
        to_date = data.get('to_date')
        
        # ✅ Fetch all customer invoices (account.move)
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('invoice_date', '>=', from_date),
            ('invoice_date', '<=', to_date),
            ('state', 'in', ['posted', 'paid']),  # only posted or paid invoices
        ])

        # ✅ Debugging output
        print(f"Fetched {len(invoices)} invoices between {from_date} and {to_date}")

        # ✅ Each invoice already contains line_ids (account.move.line)
        # You can access via invoice.line_ids
        for inv in invoices:
            print(f"Invoice: {inv.name}, Lines: {len(inv.invoice_line_ids)}")

        other = {
            'date_from': data.get('from_date'),
            'date_to': data.get('to_date'),
        }
        return {
            'others': other,
            'data': invoices,
        }

        
