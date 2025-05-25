from odoo import models, fields


class FormeJuridique(models.Model):
    _name = 'forme.juridique'
    _description = "Forme juridique"

    name = fields.Char(
        string="Nom",
        required=True
    )
    code = fields.Char(
        string="Code"
    )
