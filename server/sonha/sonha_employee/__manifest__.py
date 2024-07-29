# -*- coding: utf-8 -*-
{
    'name': 'Employee Son Ha',
    'version': '1.7',
    'category': 'Human Resources',
    'summary': 'Son ha Employee',
    'website': 'https://',
    'description': "Employee Son Ha",
    'depends': ['hr', 'base'],
    'data': [
        'security/sonha_employee_security.xml',
        'security/ir.model.access.csv',
        'views/sonha_employee_views.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
