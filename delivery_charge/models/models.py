# -*- coding: utf-8 -*-

from odoo import models, fields, api


class website_form_model(models.Model):
    _inherit = 'ir.model'

    def _get_form_writable_fields(self):
        """
        Restriction of "authorized fields" (fields which can be used in the
        form builders) to fields which have actually been opted into form
        builders and are writable. By default no field is writable by the
        form builder.
        """
        included = {
            field.name
            for field in self.env['ir.model.fields'].sudo().search([
                '|',
                '&',
                ('model_id', '=', self.id),
                ('website_form_blacklisted', '=', False),
                '&',
                ('name', '=', 'delivery_charge_id'),
                ('model', 'in', ['res.partner']),
            ])
        }
        return {
            k: v for k, v in self.get_authorized_fields(self.model).items()
            if k in included
        }
