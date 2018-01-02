# -*- coding: utf-8 -*-
# Copyright 2016 SYLEAM Info Services
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    writeoff_account_id = fields.Many2one(comodel_name='account.account', string='Write-Off account')
    payment_method_id = fields.Many2one(
        comodel_name='account.payment.method', string='Payment method',
        required=False, default=lambda self: self.env.ref(
            'account.account_payment_method_manual_in'))
