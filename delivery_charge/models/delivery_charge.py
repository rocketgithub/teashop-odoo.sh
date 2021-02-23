# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _


class DeliveryCharge(models.Model):
    _name = 'delivery.charge'
    _order = 'sequence'

    name = fields.Char('Area Name', required=True)
    sequence = fields.Integer('Sequence')
    charge = fields.Float('Charge')
    min_order_amount = fields.Float('Min Order Value')
    amount_with_discount = fields.Float('Amount with discount')
