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

from openerp import models, api, fields


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    payment_ids = fields.One2many(comodel_name='account.payment', inverse_name='transaction_id', string='Payments')

    @api.multi
    def write(self, vals):
        result = super(PaymentTransaction, self).write(vals)
        for transaction in self:
            if transaction.state == 'done'\
               and transaction.acquirer_id.payment_mode == 'auto':
                transaction.create_account_payment()
        return result

    @api.multi
    def create_account_payment(self):
        self.ensure_one()
        self.env['account.payment'].create({
            'payment_date': fields.Date.context_today(self),
            'payment_type': 'inbound',
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'journal_id': self.acquirer_id.journal_id.id,
            'partner_type': 'customer',
            'partner_id': self.partner_id.id,
            'payment_reference': self.reference,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            'transaction_id': self.id,
        }).post()
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
