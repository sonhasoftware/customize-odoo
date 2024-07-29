# -*- coding: utf-8 -*-
{
    'name': 'Power Sonha',
    'version': '1.0',
    'category': 'Power',
    'summary': 'Power',
    'website': 'https://',
    'description': "Power",
    'depends': ['base', 'hr', 'web'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/data_bi_views.xml',
        'views/views.xml',
    ],
    'qweb': [
        'sonha_powerbi/static/src/xml/column_chart_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
