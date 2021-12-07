{
    "name": "Procurement per BoM",
    "version": "14",
    "summary": "Shows stock availability per BoM",
    "author": "Norair Arutshyan",
    "depends": [
        "base",
        'web',
        "stock",
        "product",
        "mrp",
    ],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_bom_procurement_view.xml',
        'views/mrp_bom_procurement_menus.xml',
    ],
}
