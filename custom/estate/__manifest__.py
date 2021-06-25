{
    'name': "Real Estate",
    'depends': [
        'base',
        'web',
        'estate_property_type',
    ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
}
