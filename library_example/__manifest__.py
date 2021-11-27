# -*- coding: utf-8 -*-
{
    'name': "library_example",
    'summary': """
       Addon de ejemplo para el modelado de una libreria
       """,
    'description': """
        Addon de ejemplo para el modelado de una libraria. Permite la gestión de librerias y libros
    """,
    'author': "equipo lojagas",
    'website': "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'purchase'],
    # always loaded
    'data': [
        'security/library_security.xml',
        'security/ir.model.access.csv',
        'reports/library_report.xml',
        'views/library_view.xml',
        'data/library_sequence.xml',
        'views/purchase_order_view.xml',
    ],

}
