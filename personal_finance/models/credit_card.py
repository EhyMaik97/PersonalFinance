from odoo import models, fields, api
import re
credit_card_regex = r'^([4-6]\d{3}[\ \-]?\d{4}[\ \-]?\d{4}[\ \-]?\d{4}|3\d{3}[\ \-]?\d{6}[\ \-]?\d{5}|6011[\ \-]?\d{4}[\ \-]?\d{4}[\ \-]?\d{4}|3(4|7)\d{2}[\ \-]?\d{6}[\ \-]?\d{5}|(352[89]|35[3-8]\d)[\ \-]?\d{4}[\ \-]?\d{4}[\ \-]?\d{4}|(?:5[1-5]|2[2-7]|222[1-9]|22[3-9]|2[3-6]\d)[\ \-]?\d{4}[\ \-]?\d{4}[\ \-]?\d{4}|(?:6[01]|636\d)[\ \-]?\d{4}[\ \-]?\d{4}[\ \-]?\d{4})$'


class CreditCard(models.Model):
    _name = 'credit.card'
    _description = 'Credit Card'

    name = fields.Char(string='Card Holder Name')
    card_number = fields.Char(string='Card Number')
    card_type = fields.Char(string='Card Type', compute='_compute_card_type', store=True)
    info_card = fields.Char(string='Card Info', compute='_compute_card_info', store=True)

    @api.depends('card_number')
    def _compute_card_type(self):
        """ Define regular expressions for different card types:
        visa_regex = '^4[0-9]{12}(?:[0-9]{3})?$'
        mastercard_regex = '^5[1-5][0-9]{14}$'
        amex_regex = '^3[47][0-9]{13}$'
        discover_regex = '^6(?:011|5[0-9]{2})[0-9]{12}$'"""

        # Define a table of IINs (Issuer Identification Numbers) for each card type
        iin_table = {
            'Visa': ['4'],
            'Mastercard': ['51', '52', '53', '54', '55'],
            'American Express': ['34', '37'],
            'Discover': ['6011', '622126', '622127', '622128', '622129', '62213',
                         '62214', '62215', '62216', '62217', '62218', '62219',
                         '6222', '6223', '6224', '6225', '6226', '6227', '6228',
                         '62290', '62291', '622920', '622921', '622922', '622923',
                         '622924', '622925', '644', '645', '646', '647', '648',
                         '649', '65'],
        }

        for rec in self:
            # Extract only the digits from the card number
            card_number = str(rec.card_number)
            card_number = re.sub(r'\D', '', card_number)

            # Validate the card number using a regular expression
            if not re.match(credit_card_regex, card_number):
                rec.card_type = 'Invalid Card Number'
                continue

            # Determine the IIN of the card number
            iin = None
            for prefix, iins in iin_table.items():
                for iin in iins:
                    if card_number.startswith(iin):
                        rec.card_type = prefix
                        break
                if rec.card_type:
                    break

            # If the IIN couldn't be determined, mark the card type as Unknown
            if not rec.card_type:
                rec.card_type = 'Unknown'

    @api.depends('card_number')
    def _compute_card_info(self):
        for rec in self:
            if rec.card_number:
                rec.info_card = '*' + rec.card_number[-4:]
            else:
                rec.info_card = False
