# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo import http,_
from odoo.http import request


class WebsiteSaleDeliveryCharge(WebsiteSale):

	@http.route()
	def address(self, **kw):
		res = super(WebsiteSaleDeliveryCharge, self).address(**kw)
		Partner = request.env['res.partner'].with_context(show_address=1).sudo()
		order = request.website.sale_get_order()

		mode = (False, False)
		def_delivery_charge_id = order.partner_id.delivery_charge_id
		values, errors = {}, {}

		partner_id = int(kw.get('partner_id', -1))

		# IF PUBLIC ORDER
		if order.partner_id.id != request.website.user_id.sudo().partner_id.id:
			if partner_id > 0:
				if mode:
					values = Partner.browse(partner_id)

		# IF POSTED
		if 'submitted' in kw:
			delivery_product = request.env.ref('delivery_charge.delivery_charge_product')
			if delivery_product and order.order_line:
				delivery_product_line = order.order_line.filtered(lambda x: x.product_id.id == delivery_product.id)
				amount_untaxed = order.amount_untaxed - (delivery_product_line.price_total or 0)
				if not def_delivery_charge_id.min_order_amount or amount_untaxed < def_delivery_charge_id.min_order_amount:
					if delivery_product_line:
						delivery_product_line.price_unit = def_delivery_charge_id.charge
					else:
						order.order_line |= order.order_line.new({
							'product_id': delivery_product.id,
							'price_unit': def_delivery_charge_id.charge
						})
				else:
					if delivery_product_line:
						delivery_product_line.unlink()

		area = 'delivery_charge_id' in values and values['delivery_charge_id'] != '' and request.env['delivery.charge'].browse(int(values['delivery_charge_id']))
		area = area and area.exists() or def_delivery_charge_id

		res.qcontext.update({
			'area': area,
			'areas': request.env['delivery.charge'].sudo().search([])
		})
		return res

	@http.route(['/shop/confirm_order'], type='http', auth="public", website=True, sitemap=False)
	def confirm_order(self, **post):
		order = request.website.sale_get_order()

		redirection = self.checkout_redirection(order)
		if redirection:
			return redirection

		order.onchange_partner_shipping_id()
		order.calculate_delivery_charge()
		order.order_line._compute_tax_id()
		request.session['sale_last_order_id'] = order.id
		request.website.sale_get_order(update_pricelist=True)
		extra_step = request.website.viewref('website_sale.extra_info_option')
		if extra_step.active:
			return request.redirect("/shop/extra_info")

		return request.redirect("/shop/payment")

	@http.route(['/shop/payment'], type='http', auth="public", website=True, sitemap=False)
	def payment(self, **post):
		""" Payment step. This page proposes several payment means based on available
		payment.acquirer. State at this point :

		 - a draft sales order with lines; otherwise, clean context / session and
		   back to the shop
		 - no transaction in context / session, or only a draft one, if the customer
		   did go to a payment.acquirer website but closed the tab without
		   paying / canceling
		"""
		order = request.website.sale_get_order()
		order.calculate_delivery_charge()
		redirection = self.checkout_redirection(order)
		if redirection:
			return redirection

		render_values = self._get_shop_payment_values(order, **post)
		render_values['only_services'] = order and order.only_services or False

		if render_values['errors']:
			render_values.pop('acquirers', '')
			render_values.pop('tokens', '')

		return request.render("website_sale.payment", render_values)
