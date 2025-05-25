# -*- coding: utf-8 -*-

{
    'name': 'Kit Fiscal Algérie | Algeria Fiscal base | Algerie fiscal 2025',
      'summary': """
            Ce module fournit les éléments fiscaux essentiels pour toute entreprise algérienne utilisant Odoo. Il permet d’enregistrer les identifiants fiscaux obligatoires (NIF, NIS, RC, AI) pour l’entreprise ainsi que pour ses clients, et offre la possibilité d’imprimer des factures conformes aux exigences de la loi de 2025.
        """,

    'description': """
   Ce module fournit les éléments fiscaux essentiels pour toute entreprise algérienne utilisant Odoo. Il permet d’enregistrer les identifiants fiscaux obligatoires (NIF, NIS, RC, AI) pour l’entreprise ainsi que pour ses clients, et offre la possibilité d’imprimer des factures conformes aux exigences légales de 2025.

Face à un durcissement du contrôle fiscal, de plus en plus d’entreprises sont sanctionnées pour des factures non conformes (absence ou mauvaise disposition des mentions obligatoires). Ce module aide à prévenir ces risques en intégrant les normes de présentation imposées par la législation.
            """,

    'author': "RAG Solutions",
    'website': "https://www.linkedin.com/in/mohamed-lahrech-787936172/",
    'category': 'Sales/Sales',
    'version': '16.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts', 'account','purchase','sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/forme_juridique_data.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'report/account_invoice_report.xml',
        # 'report/header_footer_inherit.xml',
        'report/purchase_order_report.xml',
        'report/sale_order_report.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'report/facture.xml',
        'report/report_facture.xml',
    ],
    'installable': True,
    'auto_install': False,
'images': [
            'static/description/banner.gif'
    ],
}
