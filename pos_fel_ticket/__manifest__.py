# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'POS Fel 58mm Ticket',
    'version': '1.0',
    'category': 'Point of Sale',
    'summary': 'Ticket de 58mm para Punto de Venta con FEL',
    'description': """

    """,
    'depends': ['pos_fel'],
    'qweb': [
        'static/src/xml/pos_fel_custom.xml',
    ],
    'installable': True,
    'auto_install': False,
}
