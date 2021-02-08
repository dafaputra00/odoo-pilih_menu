# -*- coding: utf-8 -*-
{
    'name': "Pilih Menu",

    'summary': """
        Aplikasi Menu Restoran""",

    'description': """
        Long description of module's purpose
    """,

    'author': "DafaPutra",
    'website': "",
    'category': 'Uncategorized',
    'version': '12.0.0',

    'depends': ['base','contacts', 'sale_management', 'point_of_sale', 'purchase', 'stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/dapur.xml',
        'views/pos_assets.xml',
    ],

    'qweb': [
        'static/src/xml/pos.xml'
     ],


    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}