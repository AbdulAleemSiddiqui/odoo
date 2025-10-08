from odoo import _, api, fields, models


class SalesReportBrandWizard(models.TransientModel):
    _name = "sales.report.brand"
    _description = "Sales Report Brand Wise"

    from_date = fields.Date(string="from date")
    to_date = fields.Date(string="to date")
    brand = fields.Selection(
        [
            ("Bulova", "Bulova"),
            ("Casio General", "Casio General"),
            ("Frederique Constant", "Frederique Constant"),
            ("G-shock", "G-shock"),
            ("Rado", "Rado"),
            ("Seiko", "Seiko"),
            ("Tissot", "Tissot"),
        ],
        string="Brand",
        required=True,
    )
    store_ids = fields.Many2many("pos.config", string="Stores", required=True)
    sales_type = fields.Selection(
        [
            ("sales", "Sales"),
            ("returns", "Sales Return"),
        ],
        string="Sales Type",
        default="sales",
        required=True,
    )

    def print_report_word(self):

        data = {
            "from_date": self.from_date,
            "to_date": self.to_date,
            "brand": self.brand,
            "store_ids": self.store_ids.ids,
            "sales_type": self.sales_type,
        }

        return (
            self.env.ref("sales_report_brand.sales_report_brand_pdf")
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
                self.brand,
                self.store_ids.ids,
                self.sales_type,
            ),
            "target": "self",
        }
