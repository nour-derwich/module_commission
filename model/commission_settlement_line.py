from odoo import api, fields, models

class CommissionSettlementLine(models.Model):
    _name = "commission.settlement.line"
    _description = "Commission Settlement Line BMG"

    settlement_id = fields.Many2one('commission.settlement', string='Settlement Reference', required=True, ondelete='cascade')
    payment_id = fields.Many2one('account.payment', string='Payment Reference', required=True)
    montant = fields.Float(string="Montant", related='payment_id.amount', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='payment_id.currency_id', store=True)
