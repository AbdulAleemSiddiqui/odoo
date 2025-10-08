from odoo import http
from odoo.http import request
import io
import xlsxwriter
import io
from odoo import http
import xlwt
import datetime

class SaleReportBrandController(http.Controller):

    @http.route('/sales_report_brand/excel', type='http', auth='user', methods=['GET'], csrf=False)
    def generate_excel_report(self, date_from, date_to, brand, store_ids,sales_type):
        store_ids_str = ""
        if store_ids != "[]":
            store_ids_str = str(store_ids).split("[")[-1].split("]")[0]
            
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


                where po.date_order >= '{date_from}' and po.date_order <= '{date_to}'
                """
                        ) 
        
        
        if brand:
            query += f""" and pt."Brand" = '{brand}'"""
        if store_ids_str:
            query += f" and po.config_id in ({store_ids_str})"
        if sales_type == 'returns':
            query += f" and po.name like '%REFUND%'"


        query += f'order by pt."Brand", pol.qty desc'
                
        
        env = http.request.env
        env.cr.execute(query)
        records = env.cr.dictfetchall()

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Sales Report Brand Wise')

        title_style = xlwt.XFStyle()
        title_font = xlwt.Font()
        title_font.bold = True
        title_font.height = 240
        title_style.font = title_font

        title_alignment = xlwt.Alignment()
        title_alignment.horz = xlwt.Alignment.HORZ_CENTER
        title_style.alignment = title_alignment

        title_pattern = xlwt.Pattern()
        title_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        title_pattern.pattern_fore_colour = xlwt.Style.colour_map['white'] 

        title_style.pattern = title_pattern


        sheet.write_merge(0, 0, 0, 8, 'Sales Report Brand Wise', title_style)

        header_style_center = xlwt.XFStyle()
        header_font = xlwt.Font()
        header_font.bold = True
        header_font.height = 200

        header_style_center.font = header_font

        header_alignment_center = xlwt.Alignment()
        header_alignment_center.horz = xlwt.Alignment.HORZ_CENTER
        header_style_center.alignment = header_alignment_center

        header_pattern = xlwt.Pattern()
        header_pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        header_pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25'] 
        header_style_center.pattern = header_pattern

        data_style_center = xlwt.XFStyle()
        data_alignment_center = xlwt.Alignment()
        data_alignment_center.horz = xlwt.Alignment.HORZ_CENTER
        data_style_center.alignment = data_alignment_center

        data_font = xlwt.Font()
        data_font.bold = True
        data_font.height = 200
        data_style_center.font = data_font

        data_style_right = xlwt.XFStyle()
        data_alignment_right = xlwt.Alignment()
        data_alignment_right.horz = xlwt.Alignment.HORZ_RIGHT
        data_style_right.alignment = data_alignment_right
        data_style_right.font = data_font


        sheet.write_merge(2, 2, 3, 4, f'Date From : {date_from}', data_style_center) 
        sheet.write_merge(2, 2, 5, 6, f'Date To : {date_to}', data_style_center)  

        data_font = xlwt.Font()
        data_font.bold = False
        data_font.height = 200
        data_style_center.font = data_font



        headers = [
                'SR#',
                'Brand',
                'Qty',
                'Return Qty',
                'Sale Price',
                'Tax',
                'Gross Amount',
                'Discount',
                'Net Amount',
            ]


        for col, header in enumerate(headers):
            sheet.write(4, col, header, header_style_center)

        row = 5
        sn = 1
        for record in records:
                line  = env['pos.order.line'].search([('id','=',record['line_id'])])

                sheet.write(row, 0, sn, data_style_center)  
                sheet.write(row, 1, record['brand_name'], data_style_center)
                sheet.write(row, 2, record['qty'], data_style_center)         
                sheet.write(row, 3, line.refunded_qty, data_style_center)     
                sheet.write(row, 4, record['price'], data_style_center)
                sheet.write(row, 5, line.price_subtotal_incl - line.price_subtotal, data_style_center)
                sheet.write(row, 6, (record['qty'] * record['price']) + (line.price_subtotal_incl - line.price_subtotal), data_style_center)
                sheet.write(row, 7, line.discount, data_style_center)
                sheet.write(row, 8, line.price_subtotal_incl, data_style_center)

                

                sn += 1
                row += 1

        stream = io.BytesIO()
        workbook.save(stream)
        stream.seek(0)

        report_name = 'Sales Report.xls'
        response = http.request.make_response(
            stream.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.ms-excel'),
                ('Content-Disposition', http.content_disposition(report_name))
            ]
        )
        response.set_cookie('fileToken', report_name)
        return response
