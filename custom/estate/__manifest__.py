{
    'name': "Real Estate",
    'depends': [
        'base',
        'web',
        'estate_property_tag',
        'estate_property_offer',
        'estate_property_type',
    ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
    ],
}
