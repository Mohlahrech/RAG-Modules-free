# -*- coding: utf-8 -*-
# from odoo import http


# class PickingWizard(http.Controller):
#     @http.route('/picking_wizard/picking_wizard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/picking_wizard/picking_wizard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('picking_wizard.listing', {
#             'root': '/picking_wizard/picking_wizard',
#             'objects': http.request.env['picking_wizard.picking_wizard'].search([]),
#         })

#     @http.route('/picking_wizard/picking_wizard/objects/<model("picking_wizard.picking_wizard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('picking_wizard.object', {
#             'object': obj
#         })
