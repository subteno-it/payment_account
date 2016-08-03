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

    payment_id = fields.Many2one(comodel_name='account.payment', string='Payment')

    @api.multi
    def write(self, vals):
        result = super(PaymentTransaction, self).write(vals)
        if not self.env.context.get('no_create_account', False):
            for transaction in self:
                if not transaction.payment_id\
                   and transaction.state == 'done'\
                   and transaction.acquirer_id.payment_mode == 'auto':
                    transaction.create_account_payment()
        return result

    @api.multi
    def create_account_payment(self):
        for transaction in self:
            account_payment = self.env['account.payment'].create({
                'payment_date': fields.Date.context_today(self),
                'payment_type': 'inbound',
                'amount': transaction.amount,
                'currency_id': transaction.currency_id.id,
                'journal_id': transaction.acquirer_id.journal_id.id,
                'partner_type': 'customer',
                'partner_id': transaction.partner_id.id,
                'payment_reference': transaction.reference,
                'payment_method_id': self.env.ref('account.account_payment_method_manual_in').id,
            })
            account_payment.post()
            transaction.with_context(no_create_account=True).write({'payment_id': account_payment.id})
        return True


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
