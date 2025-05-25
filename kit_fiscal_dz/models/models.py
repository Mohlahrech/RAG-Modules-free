# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        compute='_compute_sale_order_id',
        store=True,  # Optional: Store the field if you need to search/group by it
        readonly=True)

    purchase_id = fields.Many2one(
        'purchase.order',
        string='Purchase Order',
        compute='_compute_purchase_id',
        store=True,
        readonly=True)

    payment_mode = fields.Selection([
        ('cheque', 'Cheque'),
        ('virement', 'Virement'),
        ('cash', 'Espèces'),
        # Add other payment modes if needed
    ], string='Mode de Paiement', default='virement') # Set a default if desired

    @api.depends('invoice_origin')
    def _compute_sale_order_id(self):
        for move in self:
            sale_order = None
            # Check if it's a customer invoice/credit note before searching SO
            if move.is_sale_document(include_receipts=True) and move.invoice_origin:
                sale_order = self.env['sale.order'].search([
                    ('name', '=', move.invoice_origin),
                    ('company_id', '=', move.company_id.id)
                ], limit=1)
            move.sale_order_id = sale_order

    @api.depends('invoice_origin')
    def _compute_purchase_id(self):
        for move in self:
            purchase_order = None
            # Check if it's a vendor bill/refund before searching PO
            if move.is_purchase_document(include_receipts=True) and move.invoice_origin:
                purchase_order = self.env['purchase.order'].search([
                    ('name', '=', move.invoice_origin),
                    ('company_id', '=', move.company_id.id)
                ], limit=1)
            move.purchase_id = purchase_order

# class facture_fiscale(models.Model):
#     _name = 'facture_fiscale.facture_fiscale'
#     _description = 'facture_fiscale.facture_fiscale'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
