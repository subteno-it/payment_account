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

from openerp import models, fields


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    journal_id = fields.Many2one(comodel_name='account.journal', string='Bank', domain=[('type', '=', 'bank')])
    payment_mode = fields.Selection(selection=[('manual', 'Manual'), ('auto', 'Auto')], default='manual', string='Payment Mode')
    writeoff_account_id = fields.Many2one(comodel_name='account.account', string='Write-Off account')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
