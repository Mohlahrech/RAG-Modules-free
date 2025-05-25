# -*- coding: utf-8 -*-

from odoo import fields, models, api
import re
from odoo.exceptions import ValidationError

GLOBAL_REGEXEX_NIS_NIF = "^[a-zA-Z0-9]{15}$"
GLOBAL_REGEXEX_NIS_NIS = "^[a-zA-Z0-9]{15}$"
GLOBAL_REGEXEX_AI = "^[a-zA-Z0-9]{11}$"


# Ajouter les données fiscales à partner (client or fournisseur)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity_conforme = fields.Char(string='Activité Conforme')

    nrc = fields.Char(
        string='N° RC',
        help="Numéro du registre de commerce"
    )
    nif = fields.Char(
        string='N.I.F',
        size=15,
        help="Numéro d’Identification Fiscal"
    )
    ai = fields.Char(
        string='A.I',
        size=11,
        help="Numéro d’Article"
    )
    nis = fields.Char(
        string='N.I.S',
        size=15,
        help="Numéro d’Identification Statistique"
    )
    fax = fields.Char(
        string='Fax',
        size=64,
        help="Fax number"
    )

    # valider le nif
    @api.constrains('nif')
    def is_valid_nif(self):
        for record in self:
            if record.nif and not re.match(GLOBAL_REGEXEX_NIS_NIF, record.nif):
                raise ValidationError("Veuillez verifier le N.I.F")

    # valider le nis
    @api.constrains('nis')
    def is_valid_nis(self):
        for record in self:
            if record.nis and not re.match(GLOBAL_REGEXEX_NIS_NIS, record.nis):
                raise ValidationError("Veuillez verifier le N.I.S")

    # valider le ai
    @api.constrains('ai')
    def is_valid_ai(self):
        for record in self:
            if record.ai and  not re.match(GLOBAL_REGEXEX_AI, record.ai):
                raise ValidationError("Veuillez verifier le A.I")
