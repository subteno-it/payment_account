# -*- coding: utf-8 -*-
##############################################################################
#
#    payment_account module for OpenERP, Allows to create account payment from payment transaction
#    Copyright (C) 2016 SYLEAM Info Services (<http://www.syleam.fr>)
#              Sebastien LANGE <sebastien.lange@syleam.fr>
#
#    This file is a part of payment_account
#
#    payment_account is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    payment_account is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
