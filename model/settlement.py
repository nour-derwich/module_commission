from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class CommissionSettlement(models.Model):
    _name = "commission.settlement"
    _description = "Commission Settlement BMG"

    state = fields.Selection(
        selection=[
            ("Non_Attribuée", "Non Attribuée"),
            ("Attribuée", "Attribuée")
        ],
        string="State Commission",
        readonly=True,
        default="Non_Attribuée",
    )
    date_from = fields.Date(string='Date Début')
    date_to = fields.Date(string='Date Fin')
    agent_id = fields.Many2one('res.users', string='Agent')
    calcul_method_id = fields.Many2one('commission', string='Méthode de calcul')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    montant_paiements = fields.Monetary(string="Montant des paiements", compute='_compute_montant_paiements')
    montant_commission = fields.Monetary(string="Montant de la commission", compute='_compute_montant_commission')
    line_ids = fields.One2many('commission.settlement.line', 'settlement_id', string='Lignes des paiements',
                               readonly=True)

    def action_confirm(self):
        self.write({'state': 'Attribuée'})

    @api.depends('line_ids')
    def _compute_montant_paiements(self):
        for record in self:
            record.montant_paiements = sum(line.montant for line in record.line_ids)

    @api.depends('calcul_method_id', 'montant_paiements')
    def _compute_montant_commission(self):
        for record in self:
            if record.calcul_method_id:
                record.montant_commission = record.calcul_method_id.montant_fixe + (
                        record.montant_paiements * record.calcul_method_id.taux_variable / 100)
            else:
                record.montant_commission = 0.0

    @api.onchange('date_from', 'date_to', 'agent_id')
    def _onchange_date_agent(self):
        if self.date_from and self.date_to and self.agent_id:
            payments = self.env['account.payment'].search([
                ('payment_date', '>=', self.date_from),
                ('payment_date', '<=', self.date_to),
                ('state', '=', 'posted'),
                ('partner_id', '=', self.agent_id.partner_id.id),
            ])

            # Debug logging
            _logger.info(f"Payments found: {payments}")

            lines = [(5, 0, 0)]  # Clear all existing lines
            for payment in payments:
                _logger.info(
                    f"Adding payment: {payment.id}, amount: {payment.amount}, currency: {payment.currency_id.id}")
                lines.append((0, 0, {
                    'payment_id': payment.id,
                    'montant': payment.amount,
                    'currency_id': payment.currency_id.id,
                }))
            self.line_ids = lines


class CommissionSettlementLine(models.Model):
    _name = "commission.settlement.line"
    _description = "Commission Settlement Line BMG"

    settlement_id = fields.Many2one('commission.settlement', string='Settlement Reference', required=True,
                                    ondelete='cascade')
    payment_id = fields.Many2one('account.payment', string='Payment Reference', required=True, readonly=True)
    montant = fields.Monetary(string="Montant", readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
