# -*- coding: utf-8 -*-

{
    'name': 'Personal Finance',
    'version': '0.0',
    'category': 'Accounting',
    'images': ['static/description/main_screenshot.png'],
    'author': 'Michelangelo Sparapano',
    'support': 'm.sparapano97@gmail.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',

        'views/personal_finance_menus.xml',
        'views/money_flow_views.xml',
        'views/money_flow_tags_views.xml',
        'views/money_flow_category_views.xml',
        'views/credit_card_view.xml',

        'report/money_flow_report.xml',
        ],
    'installable': True,
    'application': True,
}
