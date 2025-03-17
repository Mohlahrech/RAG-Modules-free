# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def open_split_wizard(self):
        """ Action to open the stock picking split wizard. """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Split Picking',
            'res_model': 'stock.picking.split.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_ids': self.ids,  # Pass the current picking record(s) to the wizard
            },
        }
