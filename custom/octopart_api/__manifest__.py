{
    "name": "Octopart API",
    "version": "14",
    "summary": "Links product with Octopart",
    "author": "Norair Arutshyan",
    "depends": [
        "base",
        'web',
        "stock",
        "product",
    ],
    'application': True,
    'data': [
        "security/ir.model.access.csv",
        "views/octopart_parts_view.xml",
        "views/octopart_availability_view.xml",
        "views/octopart_manufacturers_view.xml",
        "views/octopart_vendors_view.xml",
        "views/product_views.xml",
        "views/octopart_menu.xml",

    ],
}
