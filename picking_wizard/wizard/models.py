# -*- coding: utf-8 -*-
from odoo import models, fields, api, Command



class StockPickingSplitWizard(models.TransientModel):
    _name = "stock.picking.split.wizard"

    line_ids = fields.One2many('stock.picking.split.wizard.line', 'wizard_id', string='Lines')

    @api.model
    def default_get(self, fields):
        ctx = self.env.context.copy()
        picking_ids = ctx.get('active_ids', [])
        stock_picking_obj = self.env['stock.picking']
        lines = []

        for picking in stock_picking_obj.browse(picking_ids):
            for move in picking.move_ids_without_package:
                lines.append({
                    'product_id': move.product_id.id,
                    'location_id': move.location_id.id,
                    'location_dest_id': move.location_dest_id.id,
                    'move_id': move.id,
                    'product_uom_qty': move.product_uom_qty,  # Keep for reference
                    'product_uom': move.product_uom.id
                })

        defaults = super(StockPickingSplitWizard, self).default_get(fields)
        defaults['line_ids'] = [(0, 0, line) for line in lines]  # Correctly format line_ids
        return defaults

    def action_split(self):
        # Iterate over each line in the wizard
        for line in self.line_ids:
            if line.move_id:
                print("nami")
                # Set the quantity_done in the stock.move record based on user input in wizard
                line.move_id.quantity_done = line.product_uom_qty
            else:
                print("chkpi")
                # Optionally update locations if necessary
        #         line.move_id.location_id = line.location_id
        #         line.move_id.location_dest_id = line.location_dest_id
        #         # Optionally, you can also call additional actions on stock.move
        #         # line.move_id._action_done()  # Uncomment to validate the move
        #
        # # Optional: Perform additional actions on stock.picking if necessary
        # picking_ids = self.env.context.get('active_ids', [])
        # for picking in self.env['stock.picking'].browse(picking_ids):
        #     # Confirm or perform any additional actions as needed
        #     picking.action_confirm()  # Confirm the picking if needed

        return {'type': 'ir.actions.act_window_close'}

class StockPickingSplitWizardLine(models.TransientModel):
    _name = 'stock.picking.split.wizard.line'

    move_id = fields.Many2one('stock.move', 'Stock Move', required=True)  # Ensure move_id is required
    product_id = fields.Many2one('product.product', 'Article', required=True)
    product_uom_qty = fields.Float('Quantité', digits=(16, 2))  # This field is for user input
    location_id = fields.Many2one('stock.location', 'Source Location', index=True)  # Optional index for performance
    location_dest_id = fields.Many2one('stock.location', 'Destination Location', required=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True)  # Ensure this is required
    wizard_id = fields.Many2one('stock.picking.split.wizard', 'Wizard')  # Ensure this is set
