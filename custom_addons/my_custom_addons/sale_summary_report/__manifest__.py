{
    'name': 'Sale Summary Report',
    'version': '1.0',
    'depends': ['account'],
    'data': [
        'report/sale_summary_report.xml',
        'report/sale_summary_template.xml',
        'views/account_move_inherit.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}