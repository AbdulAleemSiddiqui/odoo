from odoo import api, fields, models

class CustomReport(models.AbstractModel):
    _name = "report.invoicing_custom_report.invoicing_custom_report_template"
    _description = "Invoicing Custom Report"

    def _get_report_values(self, docids, data=None):
        from_date = data.get('from_date')
        to_date = data.get('to_date')

        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('invoice_date', '>=', from_date),
            ('invoice_date', '<=', to_date),
            ('state', 'in', ['posted', 'paid']),
        ])

        report_lines = []
        counter = 1

        for inv in invoices:
            currency = inv.currency_id  # get currency for proper rounding
            for line in inv.invoice_line_ids:
                taxes_data = line.tax_ids.compute_all(
                    line.price_unit,
                    currency,
                    line.quantity,
                    product=line.product_id,
                    partner=inv.partner_id
                )

                # Initialize tax amounts
                s_tax = 0.0
                further_tax = 0.0
                adv_tax = 0.0

                # Map taxes dynamically by name
                for tax in taxes_data['taxes']:
                    name = tax.get('name', '').strip().lower()
                    amount = tax.get('amount', 0.0)
                    if 'advance tax' in name:
                        adv_tax += amount
                    elif '%' in name:  # assume percentage-based tax is S.Tax
                        s_tax += amount
                    elif 'further tax' in name:
                        further_tax += amount

                # Compute and round amounts
                exclusive_amount = round(line.price_subtotal, currency.decimal_places)
                inclusive_amount = round(line.price_total, currency.decimal_places)
                discount_amount = round(line.price_unit * line.quantity * (line.discount / 100), currency.decimal_places)
                s_tax = round(s_tax, currency.decimal_places)
                further_tax = round(further_tax, currency.decimal_places)
                adv_tax = round(adv_tax, currency.decimal_places)
                net_amount = round(exclusive_amount + s_tax + further_tax + adv_tax, currency.decimal_places)

                report_lines.append({
                    's_no': counter,
                    'inv_date': inv.invoice_date,
                    'inv_number': inv.name,
                    'product_name': line.product_id.display_name,
                    'quantity': round(line.quantity, 2),
                    'exclusive_amount': exclusive_amount,
                    's_tax': s_tax,
                    'further_tax': further_tax,
                    'adv_tax': adv_tax,
                    'inclusive_amount': inclusive_amount,
                    'discount': discount_amount,
                    'net_amount': net_amount,
                })
                print(report_lines[counter - 1])  # Debug print

                counter += 1

        other = {
            'date_from': from_date,
            'date_to': to_date,
        }

        return {
            'others': other,
            'data': report_lines,
        }
