# -*- coding: utf-8 -*-


{
    'name': 'POS G4S - Get NIT',
    'version': '13.0.0.3',
    'category': 'Point Of Sale',
    'summary': 'POS G4S - Get NIT',
    'description': """POS G4S - Get NIT""",
    'author': 'Piensom',
    'website': 'piensom.com',
    'depends': ['fel_g4s', 'point_of_sale'],
    'data': [
        # Views
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'application': True,
}
