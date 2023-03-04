# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from random import randint


class MoneyFlowTags(models.Model):
    """ Tags of Money Flow's line """
    _name = "money.flow.tags"
    _description = "MoneyFlow Tags"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(
        string='Name',
        required=True
    )

    color = fields.Integer(
        string='Color',
        default=_get_default_color
    )

    _sql_constraints = [
        ('name_uniq', 'unique (name)', _("Tag name already exists!"))
    ]
