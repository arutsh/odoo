{
    'name': "Real Estate property Offer",
    'depends': [
        'base',
        'web',
        'estate'
    ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_offer_views.xml',
    ],
}
