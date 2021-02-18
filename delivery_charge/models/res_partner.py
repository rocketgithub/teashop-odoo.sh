# -*- coding: utf-8 -*-
from odoo import api, models, fields, _


class Partner(models.Model):
    _inherit = 'res.partner'

    delivery_charge_id = fields.Many2one('delivery.charge', string='Area')
