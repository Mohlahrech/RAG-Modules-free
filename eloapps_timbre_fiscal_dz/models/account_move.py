# -*- encoding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from odoo.http import request


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    def get_default_payment_type(self):
        if not self.env.registry.ready:
            return False
        return self.env['account.payment.mode'].search([('mode_type', '=', 'bank')], limit=1).id


    payment_mode = fields.Many2one(
        'account.payment.mode',
        string="Mode de paiement",
        default=get_default_payment_type
    )

    amount_timbre = fields.Monetary(
        string='Droit de timbre',
        readonly=True,
        compute='_compute_amount_timbre',
        store=True,
    )

    total_timbre = fields.Monetary(
        string='Montant avec timbre',
        readonly=True,
        compute='_compute_amount_timbre',
        store=True
    )

    payment_mode_type = fields.Char("Type")

    montant_en_lettre = fields.Boolean(
        string="Afficher le montant en lettre sur l’impression des factures",
        compute='get_timbre_montant_en_lettre',
    )

    based_on_related = fields.Selection(string='Based', related="company_id.based_on")

    def compute_based_on_related(self):
        conf = self.env['res.config.settings'].sudo().search([], order='id desc', limit=1)
        if conf.based_on == "posted_invoices":
            self.based_on_related = True
        else:
            self.based_on_related = False

    @api.onchange('payment_mode')
    def _onchange_payment_mode(self):
        for record in self:
            if record.payment_mode.mode_type != 'cash':
                company = self.env['res.company'].search([('id', 'in', self.get_current_company_value())], limit=1)
                company_id = company or self.company_id
                for line in self.line_ids:
                    if line.account_id == company_id.sale_timbre:
                        self.line_ids -= line
            if record.payment_mode.mode_type == 'cash':
                if not record.company_id.sale_timbre:
        
                    raise ValidationError(_('Verifier si les comptes contrepartie sont rempli sur la configuration de timbre'))

            record.payment_mode_type = record.payment_mode.mode_type if record.payment_mode else False

    def _timbre(self, amount_total):
        timbre = 0.0
        if self.payment_mode and self.payment_mode.mode_type == "cash":
            company = self.env['res.company'].search([('id', 'in', self.get_current_company_value())], limit=1)
            company_id = company or self.company_id
            timbre = company_id._timbre(amount_total)
        return timbre

    @api.depends('payment_mode', 'invoice_line_ids')
    def _compute_amount_timbre(self):
        for record in self:
            if record.move_type in ['out_invoice', 'out_refund']:
                if record.payment_mode.mode_type != 'cash':
                    record.amount_timbre = 0
                    record.total_timbre = 0
                    record._recompute_timbre()
                else:
                    total = record.amount_total_signed
                    if record.tax_totals:
                        if record.tax_totals['amount_total'] != 0:
                            total = record.tax_totals['amount_total']
                    print('totalllllll', total)
                    print('totalllllll', record.amount_total_signed)
                    record.amount_timbre = record._timbre(total)
                    record.total_timbre = total + record.amount_timbre if record.amount_timbre else 0.0
                    record._recompute_timbre()


    # def write(self, vals):
    #     res = super(AccountInvoice, self).write(vals)
    #     for rec in self:
    #         #if 'montant_avec_timbre' in vals 'payment_mode' in vals or 'payment_mode_supplier' in vals or 'amount_total' in vals:
    #         if 'amount_timbre' in vals:
    #             print(vals['amount_timbre'])
    #             print(rec.amount_timbre)
    #             timbre = vals['amount_timbre']
    #             if timbre > rec.company_id.mnt_max:
    #                 raise UserError(
    #                     _('Le montant du timbre est supérieur à %s, vous ne pouvez pas passer cette facture en mode espèce.\n Montant du timbre : %s',
    #                       rec.company_id.mnt_max, timbre))
    #
    #             if timbre <= rec.company_id.mnt_min:
    #                 rec.amount_timbre = rec.mnt_min
    #     return res

    @api.depends('payment_mode')
    def get_timbre_montant_en_lettre(self):
        for record in self:
            logic = False

            if record.payment_mode and record.payment_mode.mode_type == "cash":
                company = self.env['res.company'].search([('id', 'in', self.get_current_company_value())], limit=1)
                company_id = company or self.company_id
                logic = company_id.montant_en_lettre
            record.montant_en_lettre = logic
           
    def custom_amount_to_text(self, montant):
        currency_id = self.currency_id or self.env.ref('base.DZD')
        res = currency_id.amount_to_text(montant)
        if round(montant % 1, 2) == 0.0:
            res += " et zéro centime"
        if montant > 1.0:
            res = res.replace('Dinar', 'Dinars')
        return res.lower().capitalize()

    def get_current_company_value(self):

        cookies_cids = [int(r) for r in request.httprequest.cookies.get('cids').split(",")] \
            if request.httprequest.cookies.get('cids') \
            else [request.env.user.company_id.id]

        for company_id in cookies_cids:
            if company_id not in self.env.user.company_ids.ids:
                cookies_cids.remove(company_id)
        if not cookies_cids:
            cookies_cids = [self.env.company.id]
        if len(cookies_cids) == 1:
            cookies_cids.append(0)
        return cookies_cids

    def _recompute_timbre(self):
        self.ensure_one()
        company = self.env['res.company'].search([('id', 'in', self.get_current_company_value())], limit=1)
        company_id = company or self.company_id
        if company_id.based_on == 'posted_invoices':
            if self.move_type in ['out_invoice', 'out_refund']:
                if self.payment_mode and self.payment_mode.mode_type == 'cash':
                    in_draft_mode = self != self._origin
                    create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create

                    #account_timbre_id = self.company_id.sale_timbre
                    account_timbre_id = company_id.sale_timbre or self.company_id.sale_timbre

                    timbre_line_vals = {
                        'name': 'Timbre' if self.move_type == 'out_invoice' else 'Droit de timbre',
                        'quantity': 1.0,
                        'account_id': account_timbre_id.id,
                        'move_id': self.id,
                        'credit':self.amount_timbre,
                    }

                    existing_timbre_line = self.invoice_line_ids.filtered(lambda line: line.account_id == account_timbre_id)

                    if not existing_timbre_line:
                        timbre_line = create_method(timbre_line_vals)
                    else:
                        if len(existing_timbre_line) > 1:
                            self.line_ids -= existing_timbre_line[0]
                        timbre_line = existing_timbre_line

                    #timbre_line = create_method(timbre_line_vals) if not existing_timbre_line else existing_timbre_line

                    existing_lines = self.line_ids.filtered(lambda line: line.account_id != account_timbre_id)
                    if self.move_type in ('out_invoice', 'in_invoice', 'out_receipt'):
                        curr_line = 'credit'
                    elif self.move_type in ('out_refund', 'in_refund', 'in_receipt'):
                        curr_line = 'debit'

                    curr_amount = sum(existing_lines.mapped(curr_line))
                    company = self.env['res.company'].search([('id', 'in', self.get_current_company_value())], limit=1)
                    timbre_line.update({
                        curr_line: company._timbre(curr_amount) or self.company_id._timbre(curr_amount),
                        # todo: lorsque la devise est differente de la devise de l'entreprise
                        # 'amount_currency': 0.0,
                    })

                else:
                    for line in self.line_ids:
                        if line.account_id == company_id.sale_timbre:
                            self.line_ids -= line

    # def _recompute_dynamic_lines(self, recompute_all_taxes=False, recompute_tax_base_amount=False):
    #
    #     for invoice in self:
    #         # verifier la/les taxe(s) avant calcule/recalcule du timbre
    #         for line in invoice.line_ids:
    #             if line.recompute_tax_line:
    #                 recompute_all_taxes = True
    #                 line.recompute_tax_line = False
    #             if recompute_all_taxes:
    #                 invoice._recompute_tax_lines()
    #             if recompute_tax_base_amount:
    #                 invoice._recompute_tax_lines(recompute_tax_base_amount=True)
    #
    #         if invoice.is_invoice(include_receipts=False):
    #             invoice._recompute_timbre()
    #
    #     return super(AccountInvoice, self)._recompute_dynamic_lines(recompute_all_taxes, recompute_tax_base_amount)
    #_

    def action_post(self):
        result = super(AccountInvoice, self).action_post()

        for inv in self:
            if inv.payment_mode.mode_type == 'cash':
                #inv._compute_amount_timbre()
                inv.amount_residual = inv.total_timbre

        return result

    def maj_amount_timbre(self):
        moves = self.env['account.move'].search([('sav_ok', '=', True)])

        for inv in moves:
            if inv.payment_mode.mode_type == 'cash':
                inv._compute_amount_timbre()

    def maj_amount_du(self):
        moves = self.env['account.move'].search([('sav_ok', '=', True)])

        for inv in moves:
            if inv.payment_mode.mode_type == 'cash' and inv.amount_residual != inv.total_timbre:
                inv.amount_residual = inv.total_timbre



