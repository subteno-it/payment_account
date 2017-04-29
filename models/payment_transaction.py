# -*- coding: utf-8 -*-
# Copyright 2016 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    payment_ids = fields.One2many(comodel_name='account.payment', inverse_name='transaction_id', string='Payments')
    payment_count = fields.Integer(string='Payment Count', help='Number of payment', compute='_compute_payment')

    @api.multi
    def _compute_payment(self):
        for transaction in self:
            transaction.payment_count = len(transaction.payment_ids)

    @api.multi
    def write(self, vals):
        result = super(PaymentTransaction, self).write(vals)
        for transaction in self:
            if not transaction.payment_ids\
               and transaction.state == 'done'\
               and transaction.acquirer_id.payment_mode == 'auto':
                transaction.create_account_payment()
        return result

    @api.multi
    def create_account_payment(self):
        self.ensure_one()
        self.env['account.payment'].create({
            'payment_date': fields.Date.context_today(self),
            'payment_type': 'inbound',
            'amount': self.amount - self.fees,
            'currency_id': self.currency_id.id,
            'journal_id': self.acquirer_id.journal_id.id,
            'partner_type': 'customer',
            'partner_id': self.partner_id.id,
            'payment_reference': self.reference,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'transaction_id': self.id,
            'communication': self.acquirer_reference or self.reference,
            'payment_difference_handling': 'reconcile',
            'writeoff_account_id': self.acquirer_id.writeoff_account_id.id,
        }).post()
        return True

