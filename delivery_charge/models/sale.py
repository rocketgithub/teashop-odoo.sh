# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _


class DeliveryCharge(models.Model):
	_inherit = 'sale.order'

	def calculate_delivery_charge(self):
		delivery_product = self.env.ref('delivery_charge.delivery_charge_product')
		for record in self:
			delivery_charge_id = record.partner_shipping_id.delivery_charge_id
			if delivery_product and record.order_line:
				delivery_product_line = record.order_line.filtered(lambda x: x.product_id.id == delivery_product.id)
				amount_untaxed = record.amount_untaxed - (delivery_product_line.price_total or 0)
				#if not delivery_charge_id.min_order_amount or amount_untaxed < delivery_charge_id.min_order_amount:
				if amount_untaxed < delivery_charge_id.min_order_amount:
					if delivery_product_line:
						#delivery_product_line.price_unit = delivery_charge_id.amount_with_discount
						delivery_product_line.price_unit = delivery_charge_id.charge
					else:
						record.order_line |= record.order_line.new({
							'product_id': delivery_product.id,
							'price_unit': 222
						})
				else:
					if delivery_product_line:
						#delivery_product_line.unlink()
						delivery_product_line.price_unit = delivery_charge_id.amount_with_discount
					else:
						record.order_line |= record.order_line.new({
							'product_id': delivery_product.id,
							'price_unit': 444
						})	


	def write(self, values):
		res = super(DeliveryCharge, self).write(values)
		if values.get('partner_shipping_id') and self._context.get('website_id'):
			self.calculate_delivery_charge()
		return res
