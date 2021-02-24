odoo.define('dapur.validate_order', function(require) {
    "use strict";
    var core = require('web.core');
    var _t = core._t;
    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var Widget = require('web.Widget');

    screens.PaymentScreenWidget.include({
        validate_order: function() {
            this._super();
            var meja = posmodel.table.id;
            // var meja_order = this.posmodel.get_table_order();
            rpc.query({
                model: 'dapur.order',
                method: 'ubahState',
                args: [meja],
            }).then(function() {
                console.log("Harusnya Sukses")
            });
        }
    });

});