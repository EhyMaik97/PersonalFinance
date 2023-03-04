# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MoneyFlowCategory(models.Model):
    """ Category of Money Flow's line """
    _name = "money.flow.category"
    _description = "MoneyFlow Category"

    name = fields.Char(
        string='Name',
        required=True
    )

    type = fields.Selection(
        string='In/Out',
        selection=[('in', 'In'), ('out', 'Out')],
        default='out',
        required=True
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', _("Category name already exists!"))
    ]
