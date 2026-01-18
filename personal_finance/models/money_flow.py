# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class MoneyFlow(models.Model):
    _name = 'money.flow'
    _order = 'issue_date desc'

    # region Default Method

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    def name_get(self):
        result = []
        for rec in self:
            name = self.category_id.name
            result.append((rec.id, name))
        return result

    # endregion

    # region Fields

    money_in_out = fields.Selection(
        string='In/Out',
        selection=[('in', 'In'), ('out', 'Out')],
        required=True,
        default='out',
    )

    tags_ids = fields.Many2many(
        comodel_name='money.flow.tags',
        string='Tags',
        domain="[('create_uid','=',uid)]",
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self._default_currency_id()
    )

    amount = fields.Float(
        string='Amount',
        required=True
    )

    description = fields.Text(
        string='Description',
    )

    money_type = fields.Selection(
        string='Money Type',
        selection=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('paypal', 'PayPal')],
        required=True,
        default='cash'
    )

    credit_card_id = fields.Many2one(
        comodel_name='credit.card',
        domain="[('create_uid','=',uid)]"
    )

    category_id = fields.Many2one(
        comodel_name='money.flow.category',
        domain="[('create_uid','=',uid)]",
        required=True
    )

    credit_card_info = fields.Char(
        related='credit_card_id.info_card',
    )

    issue_date = fields.Datetime(
        string='Issue date',
        default=fields.Datetime.now,
        required=True
    )

    # endregion

    # region Methods

    @api.model
    def create(self, vals_list):
        res = super(MoneyFlow, self).create(vals_list)
        if res['money_in_out'] == 'out':
            res['amount'] = -res['amount']
        return res

    def write(self, vals):
        res = super(MoneyFlow, self).write(vals)
        if vals.get('money_in_out'):
            self.amount = -self.amount
        return res

    @api.onchange('money_in_out')
    def _onchange_money_in_out(self):
        self.category_id = False
        categories = self.env['money.flow.category'].search([('type', '=', self.money_in_out), ('create_uid', '=', self._uid)])
        res = {'domain': {'category_id': [('id', 'in', categories.ids)]}}
        return res
    # endregion
