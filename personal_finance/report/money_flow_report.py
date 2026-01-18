from odoo import fields, models, tools, api


class MoneyFlowReport(models.Model):
    _name = 'money.flow.report'
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    date = fields.Datetime(
        string='Issue Date',
        readonly=True
    )

    # TODO PREVEDERE NEI REPORT
    # tags_ids = fields.Many2many(
    #     comodel_name='money.flow.tags',
    #     relation='money_flow_tags_rel',
    #     column1='money_flow_id',
    #     column2='money_flow_tag_id',
    #     string='Tags',
    # )

    money_in_out = fields.Selection(
        string='In/Out',
        selection=[('in', 'In'), ('out', 'Out')],
        readonly=True
    )

    money_type = fields.Selection(
        string='Money Type',
        selection=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('paypal', 'PayPal')],
        readonly=True
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True
    )

    category_id = fields.Many2one(
        comodel_name='money.flow.category',
        string='Category',
        readonly=True
    )

    amount = fields.Float(
        string='Amount',
        readonly=True
    )

    def _select(self):
        return """
            SELECT
                mf.id,
                mf.issue_date as date,
                mf.money_in_out,
                mf.money_type,
                mf.category_id,
                mf.amount,
                mf.currency_id
        """

    def _from(self):
        return """
            FROM money_flow as mf
        """

    def _where(self):
        return """"""

    def _group_by(self):
        return """
            GROUP BY
                mf.id,
                mf.issue_date,
                mf.money_in_out,
                mf.money_type,
                mf.category_id,
                mf.amount,
                mf.currency_id
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._where(), self._group_by()))
