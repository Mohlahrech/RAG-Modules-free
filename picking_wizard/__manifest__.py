# -*- coding: utf-8 -*-
{
    'name': "Picking Wizard",

    'summary': """Edit the picking lines directly from the tree view""",

    'description': """
        This module allows you to edit the picking lines using a wizard in the list view without opening the record
    """,

    'author': "RAG Solutions",
    'website': "https://www.linkedin.com/in/mohamed-lahrech-787936172/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '15.0.1.0.0',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'images': [
                'static/description/banner.gif','static/description/banner2.gif'
        ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
