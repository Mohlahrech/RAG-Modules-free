# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re

# regular expression to validate NIF
GLOBAL_REGEXEX_NIS_NIF = "^[a-zA-Z0-9]{15}$"


class ResCompany(models.Model):
    _inherit = 'res.company'

    activity = fields.Char(
        string="Activité légale",
        size=64
    )

    capital_social = fields.Float(
        string="Capitale Social",
        digits='Account',
        required=True
    )
    fax = fields.Char(
        string="Fax",
        size=64
    )
    nrc = fields.Char(
        string="N° RC",
        size=64,
        help="Numéro du registre de commerce"
    )
    nif = fields.Char(
        string="N.I.F",
        size=15,
        help="Numéro d'identification fiscal",
    )
    ai = fields.Char(
        string="A.I",
        size=11,
        help="Numéro d’Article",
    )

    nis = fields.Char(
        string="N.I.S",
        size=15,
        help="Numéro d'identification statistique"
    )

    forme_juridique_company = fields.Many2one(
        comodel_name='forme.juridique',
        string='Forme Juridique'
    )

    @api.constrains('nif')
    def is_valid_nif(self):
        for record in self:
            if record.nif and not re.match(GLOBAL_REGEXEX_NIS_NIF, record.nif):
                raise ValidationError("Veuillez verifier le N.I.F")

    @api.constrains('nis')
    def is_valid_nis(self):
        for record in self:
            if record.nis and not re.match(GLOBAL_REGEXEX_NIS_NIF, record.nis):
                raise ValidationError("Veuillez verifier le N.I.S")
