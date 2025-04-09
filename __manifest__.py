{
    "name": "Gestion de ventas",
    "depends": [
        'base',
        'mail',
        'hr',
        'product',
        'account',
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sales_managment_views.xml",
        "views/sales_dashboard.xml"
    ],
    "assets": {
        "web.assets_backend": [
            "gestion_ventas/static/src/css/styles.css",
        ],
    },
    "application": True,
}
