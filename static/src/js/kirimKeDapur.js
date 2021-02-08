odoo.define('dapur.tombol', function(require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var gui = require('point_of_sale.gui');
    var PopupWidget = require('point_of_sale.popups');
    var qweb = core.qweb;
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');
    var pos_screens = require('point_of_sale.screens');
    var Widget = require('web.Widget');

    var dapur_button = screens.ActionButtonWidget.extend({
        template: 'BtnDapur',
        button_click: function() {
            var self = this;
            var new_quotation = [];
            var fields = _.find(this.pos.models, function(model) { return model.model === 'dapur.order'; }).fields;
            var line_fields = _.find(this.pos.models, function(model) { return model.model === 'dapur.order.line'; }).fields;
            var order = this.pos.get_order();
            var so_val = order.export_as_JSON();
            var order_lines = this.pos.get_order().get_orderlines();
            var fields = {};
            self.$('.booking_field').each(function(idx, el) {
                fields[el.name] = el.value || false;
            });
            var value = {
                state_dapur: true
            };
            fields.options = value;
            var state_dapur = fields.options.state_dapur

            so_val.state_dapur = state_dapur;
            rpc.query({
                    model: 'dapur.order',
                    method: 'create_from_ui',
                    args: [so_val],
                })
                .then(function(order) {
                    rpc.query({
                            model: 'dapur.order',
                            method: 'search_read',
                            args: [
                                [
                                    ['id', '=', order['id']]
                                ], fields
                            ],
                            limit: 1,
                        })
                        .then(function(quotation) {
                            self.pos.quotations.push(quotation[0]);
                            for (var line in quotation[0]['lines']) {
                                rpc.query({
                                    model: 'dapur.order.line',
                                    method: 'search_read',
                                    args: [
                                        [
                                            ['id', '=', quotation[0]['lines'][line]]
                                        ], line_fields
                                    ],
                                    limit: 1,
                                }).then(function(quotation_line) {
                                    self.pos.quotation_lines.push(quotation_line[0]);
                                });
                            }
                        });
                    // document.location.reload();
                    alert('Order Dikirim Ke Dapur')
                });
        }
    });

    screens.define_action_button({
        'name': 'dapur_btn',
        'widget': dapur_button
    });

    screens.OrderWidget.include({
        update_summary: function() {
            this._super();
            var changes = this.pos.get_order();
            var buttons = this.getParent().action_buttons;
            if (changes.orderlines.length != 0) {
                if (buttons && buttons.dapur_btn) {
                    buttons.dapur_btn.highlight(changes);
                }
            } else if (buttons && buttons.dapur_btn) {
                buttons.dapur_btn.highlight();
            }
        },
    });


});