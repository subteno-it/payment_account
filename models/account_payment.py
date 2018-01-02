# -*- coding: utf-8 -*-
# Copyright 2016 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    @api.onchange('payment_transaction_id')
    def _onchange_payment_transaction_id(self):
        if self.payment_transaction_id:
            transaction = self.payment_transaction_id
            self.partner_id = transaction.partner_id
            self.amount = transaction.amount
            self.currency_id = transaction.currency_id
            self.journal_id = transaction.acquirer_id.journal_id
            self.communication = transaction.acquirer_reference or transaction.reference

    @api.multi
    def validate_payment(self):
        self.payment_transaction_id.state = 'done'
        self.post()
        return True

    @api.one
    @api.depends('payment_transaction_id', 'invoice_ids', 'amount', 'payment_date', 'currency_id')
    def _compute_payment_difference(self):
        if self.payment_transaction_id:
            self.update({'payment_difference': self.payment_transaction_id.amount - self.amount})
        else:
            return super(AccountPayment, self)._compute_payment_difference()
