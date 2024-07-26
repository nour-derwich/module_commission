from odoo import api, fields, models


class CommissionBmg(models.Model):
    _name = "commission"
    _description = "Commission BMG"

    name = fields.Char(string="Nom de la méthode", required=True)
    montant_fixe = fields.Float(string="Montant fixe de la commission")
    taux_variable = fields.Float(string="Taux variable de la commission")
