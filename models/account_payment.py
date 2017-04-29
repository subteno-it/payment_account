# -*- coding: utf-8 -*-
# Copyright 2016 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    transaction_id = fields.Many2one(comodel_name='payment.transaction', string='Payment Transaction')

    @api.onchange('transaction_id')
    def _onchange_transaction_id(self):
        if self.transaction_id:
            transaction = self.transaction_id
            self.partner_id = transaction.partner_id
            self.amount = transaction.amount
            self.currency_id = transaction.currency_id
            self.journal_id = transaction.acquirer_id.journal_id
            self.communication = transaction.acquirer_reference or transaction.reference

    @api.multi
    def validate_payment(self):
        self.transaction_id.state = 'done'
        self.post()
        return True

    @api.one
    @api.depends('transaction_id', 'invoice_ids', 'amount', 'payment_date', 'currency_id')
    def _compute_payment_difference(self):
        if self.transaction_id:
            self.update({'payment_difference': self.transaction_id.amount - self.amount})
        else:
            return super(AccountPayment, self)._compute_payment_difference()

