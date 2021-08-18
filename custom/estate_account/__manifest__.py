{
    'name': "Real Estate accounting",
    'depends': [
        'base',
        'web',
        'estate',
        'account',
    ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_account_views.xml',
        'views/estate_account_menus.xml',
    ],
}
