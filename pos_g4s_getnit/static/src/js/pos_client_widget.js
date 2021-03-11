odoo.define("pos_client_widget.ClientListScreenWidgetInh", function(require) {
    "use strict";

    var core = require('web.core');
    var rpc = require('web.rpc');
    var screens = require('point_of_sale.screens');

    var QWeb = core.qweb;
    var _t = core._t;

    screens.ClientListScreenWidget.include({
        get_nit_client_details: function(partner) {
            var self = this;
            var contents = this.$('.client-details-contents');
            var $ClientName = contents.find('.client-name');

            var fields = {};
            this.$('.client-details-contents .detail').each(function(idx,el){
                if (el.name == 'vat'){
                    if (self.integer_client_details.includes(el.name)){
                        var parsed_value = parseInt(el.value, 10);
                        if (isNaN(parsed_value)){
                            fields[el.name] = false;
                        }
                        else{
                            fields[el.name] = parsed_value
                        }
                    }
                    else{
                        fields[el.name] = el.value || false;
                    }
                }
            });

            if('vat' in fields && !fields.vat){
                this.gui.show_popup('error',_t('Please Enter VAT Number To Fetch Name'));
                return;
            }
            else{
                rpc.query({
                    model: 'res.partner',
                    method: 'get_nit_name_from_vat',
                    args: [false, fields.vat],
                })
                .then(function(result_dict){
                    if (result_dict && 'name' in result_dict){
                        fields.name = result_dict.name
                        $ClientName.val(result_dict.name)
                    }
                    else{
                        self.gui.show_popup('error',_t(result_dict.error));
                        return;
                    }
                });
            }
        },

        display_client_details: function(visibility,partner,clickpos){
            var self = this;
            var searchbox = this.$('.searchbox input');
            var contents = this.$('.client-details-contents');
            var parent   = this.$('.client-list').parent();
            var scroll   = parent.scrollTop();
            var height   = contents.height();

            contents.off('click','.button.edit'); 
            contents.off('click','.button.save'); 
            contents.off('click','.button.undo'); 
            contents.off('click','.button.get_nit'); 
            contents.on('click','.button.edit',function(){ self.edit_client_details(partner); });
            contents.on('click','.button.save',function(){ self.save_client_details(partner); });
            contents.on('click','.button.undo',function(){ self.undo_client_details(partner); });
            contents.on('click','.button.get_nit',function(){ self.get_nit_client_details(partner); });
            this.editing_client = false;
            this.uploaded_picture = null;

            if(visibility === 'show'){
                contents.empty();
                contents.append($(QWeb.render('ClientDetails',{widget:this,partner:partner})));

                var new_height   = contents.height();

                if(!this.details_visible){
                    // resize client list to take into account client details
                    parent.height('-=' + new_height);

                    if(clickpos < scroll + new_height + 20 ){
                        parent.scrollTop( clickpos - 20 );
                    }else{
                        parent.scrollTop(parent.scrollTop() + new_height);
                    }
                }else{
                    parent.scrollTop(parent.scrollTop() - height + new_height);
                }

                this.details_visible = true;
                this.toggle_save_button();
            } else if (visibility === 'edit') {
                // Connect the keyboard to the edited field
                if (this.pos.config.iface_vkeyboard && this.chrome.widget.keyboard) {
                    contents.off('click', '.detail');
                    searchbox.off('click');
                    contents.on('click', '.detail', function(ev){
                        self.chrome.widget.keyboard.connect(ev.target);
                        self.chrome.widget.keyboard.show();
                    });
                    searchbox.on('click', function() {
                        self.chrome.widget.keyboard.connect($(this));
                    });
                }

                this.editing_client = true;
                contents.empty();
                contents.append($(QWeb.render('ClientDetailsEdit',{widget:this,partner:partner})));
                this.toggle_save_button();

                // Browsers attempt to scroll invisible input elements
                // into view (eg. when hidden behind keyboard). They don't
                // seem to take into account that some elements are not
                // scrollable.
                contents.find('input').blur(function() {
                    setTimeout(function() {
                        self.$('.window').scrollTop(0);
                    }, 0);
                });

                contents.find('.client-address-country').on('change', function (ev) {
                    var $stateSelection = contents.find('.client-address-states');
                    var value = this.value;
                    $stateSelection.empty()
                    $stateSelection.append($("<option/>", {
                        value: '',
                        text: 'None',
                    }));
                    self.pos.states.forEach(function (state) {
                        if (state.country_id[0] == value) {
                            $stateSelection.append($("<option/>", {
                                value: state.id,
                                text: state.name
                            }));
                        }
                    });
                });

                contents.find('.image-uploader').on('change',function(event){
                    self.load_image_file(event.target.files[0],function(res){
                        if (res) {
                            contents.find('.client-picture img, .client-picture .fa').remove();
                            contents.find('.client-picture').append("<img src='"+res+"'>");
                            contents.find('.detail.picture').remove();
                            self.uploaded_picture = res;
                        }
                    });
                });
            } else if (visibility === 'hide') {
                contents.empty();
                parent.height('100%');
                if( height > scroll ){
                    contents.css({height:height+'px'});
                    contents.animate({height:0},400,function(){
                        contents.css({height:''});
                    });
                }else{
                    parent.scrollTop( parent.scrollTop() - height);
                }
                this.details_visible = false;
                this.toggle_save_button();
            }
        },
    });
});
