{
    "name": "Stock enhancement extra",
    "version": "14",
    "summary": "Addon module for stock forecast enhancement",
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
        "security/ir.model.access.csv",
        "reports/report_stock_forecast_extra.xml",
    ],
}
