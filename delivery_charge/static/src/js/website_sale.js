odoo.define('delivery_charge.website_sale', function (require) {
    'use strict';

    const publicWidget = require('web.public.widget');

    publicWidget.registry.websiteSaleCart.include({
        _onClickChangeShipping: function (ev) {
            var $old = $('.all_shipping').find('.card.border.border-primary');
            $old.find('.btn-ship').toggle();
            $old.addClass('js_change_shipping');
            $old.removeClass('border border-primary');

            var $new = $(ev.currentTarget).parent('div.one_kanban').find('.card');
            $new.find('.btn-ship').toggle();
            $new.removeClass('js_change_shipping');
            $new.addClass('border border-primary');

            var $form = $(ev.currentTarget).parent('div.one_kanban').find('form.d-none');
            $.post($form.attr('action'), $form.serialize() + '&xhr=1').then(() => {
                window.location.reload();
            });
        },
    });
});
