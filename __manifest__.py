# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'module de Commission bmg',
    'version': '1.1',
    'summary': """""",
    'sequence': 10,
    'author': 'BMG Tech',
    'description': "Modules BMG Technologies to manage commissions",
    'category': 'Accounting/Accounting',
    'website': 'www.bmgtech.tn',
    'website': 'https://www.odoo.com/page/billing',
    'depends': ['base', 'product', 'mrp', 'stock', 'sale', ],
    'data': [
        'security/ir.model.access.csv',
        'views/commission_views.xml',


    ],

    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
