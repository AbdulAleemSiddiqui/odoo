from odoo import _, api, fields, models


class InvoicingCustomReportWizard(models.TransientModel):
    _name = "invoicing.custom.report"
    _description = "Invoicing Custom Report Wizard"

    from_date = fields.Date(string="from date")
    to_date = fields.Date(string="to date")


    def print_report_word(self):

        data = {
            "from_date": self.from_date,
            "to_date": self.to_date,
        }

        return (
            self.env.ref("invoicing_custom_report.invoicing_custom_report_pdf")
            .with_context(landscape=True)
            .report_action(self, data=data)
        )

    def print_report_excel(self):

        return {
            "type": "ir.actions.act_url",
            "url": "/sales_report_brand/excel?date_from=%s&date_to=%s&brand=%s&store_ids=%s&sales_type=%s&"
            % (
                self.from_date,
                self.to_date,
            ),
            "target": "self",
        }
