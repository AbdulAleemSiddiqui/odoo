from odoo.exceptions import UserError, AccessError
from odoo import _, api, fields, models



class CustomReport(models.AbstractModel):
    _name = "report.sales_report_brand.sales_report_brands"
    _description = "Sales Report Brand Wise"

    def _get_report_values(self, docids, data=None):
        
        brand = data['brand']
        store_ids_str = ""
        if data['store_ids'] != "[]":
            store_ids_str = str(data['store_ids']).split("[")[-1].split("]")[0]
            
        query = (f""" 
                select
                pt."Brand" as brand_name,
                pol.qty as qty,
                pol.price_unit as price,
                pol.id as line_id
                
                
                from pos_order po
                left join pos_order_line pol on pol.order_id = po.id
                left join product_product pp on pp.id = pol.product_id
                left join product_template pt on pt.id = pp.product_tmpl_id

                where po.date_order >= '{data.get('from_date')}' and po.date_order <= '{data.get('to_date')}'
                """
                        ) 
        
        
        if brand:
            query += f""" and pt."Brand" = '{brand}'"""
        if store_ids_str:
            query += f" and po.config_id in ({store_ids_str})"
        if data['sales_type'] == 'returns':
            query += f" and po.name like '%REFUND%'"


        query += f"""order by pt."Brand", pol.qty desc"""
                
        cr = self._cr
        cr.execute(query)
        result = cr.dictfetchall()
        
        other = {
            'date_from': data.get('from_date'),
            'date_to': data.get('to_date'),
        }
        return {
            'others': other,
            'data': result,
        }

        
