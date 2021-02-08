// odoo.define('disable_discount_btn', function(require) {
//     'use strict';
//     var screens = require('point_of_sale.screens');
//     screens.NumpadWidget.include({
//         renderElement: function() {
//             this._super();
//             this.$el.find('.mode-button[data-mode="discount"]').prop('disabled', true);
//             this.$el.find('.mode-button[data-mode="price"]').prop('disabled', true);
//         }
//     });
// });