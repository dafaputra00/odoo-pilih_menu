
from odoo import models, fields, api
from functools import partial


class dapur(models.Model):
    _name = 'dapur.order'

    @api.model
    def _order_fields(self, ui_order):
        process_line = partial(self.env['dapur.order.line']._order_line_fields)
        return {
            'lines': [process_line(l) for l in ui_order['lines']] if ui_order['lines'] else False,
            'table_id': ui_order['table_id'] or False,
            # 'partner_id': ui_order['partner_id'] or False,
            # 'date_order': ui_order['date_order'],
            # 'phone': ui_order['phone'],
            # 'pickup_date': ui_order['pickup_date'],
            # 'deliver_date': ui_order['deliver_date'],
            # 'delivery_address': ui_order['delivery_address'],
            # 'note': ui_order['note'] or '',
            # 'pricelist_id': ui_order['pricelist_id'] or '',
            'state_dapur': ui_order['state_dapur'] or '',
        }


    # def _default_pricelist(self):
    #     return self._default_session().config_id.pricelist_id

    name = fields.Char(string='Dapur Ref', required=True, readonly=True, copy=False, default='/')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)
    date_quotation = fields.Datetime(string='Quotation Date',
                                     readonly=True, index=True, default=fields.Datetime.now)
    # date_order = fields.Date(string='Order Date',
    #                          readonly=True, index=True, default=fields.Datetime.now)
    # amount_tax = fields.Float(compute='_compute_amount_all', string='Taxes', digits=0, default=1.2)
    # amount_total = fields.Float(compute='_compute_amount_all', string='Total', digits=0)
    lines = fields.One2many('dapur.order.line', 'order_id', string='Order Lines', copy=True)
    # partner_id = fields.Many2one('res.partner', string='Customer', change_default=True, index=True)
    table_id = fields.Many2one('restaurant.table', string='Table', help='The table where this order was served')
    state = fields.Selection([('draft', 'New'), ('done', 'Done')],
                             'Status', readonly=True, copy=False, default='draft')
    # note = fields.Text(string='Internal Notes')
    # fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position')
    # book_order_ref = fields.Char(string='Booked Order Ref', readonly=True, copy=False)
    dapur_order_ref = fields.Char(string='Booked Order Ref', readonly=True, copy=False)
    # pickup_date = fields.Datetime(string='Pickup Date', readonly=True)
    # deliver_date = fields.Datetime(string='Deliver Date', readonly=True)
    # phone = fields.Char('Contact no', help='Phone of customer for delivery')
    # delivery_address = fields.Char('Delivery Address', help='Address of customer for delivery')
    # book_order = fields.Boolean('Booking Order', readonly=True)
    state_dapur = fields.Boolean('Kirim ke dapur', readonly=True)
    # pricelist_id = fields.Many2one('product.pricelist', string='Pricelist',
    #                                default=_default_pricelist)

    # orderan = fields.Many2one('pos.order', string='Orderan')
    # status_order = fields.Selection(string='status bayar', related="orderan.state")


    # @api.onchange('status_order')
    # def cekBayar(self):
    #     if self.status_order == 'paid':
    #         self.write({'state_order', '=', False})

    @api.model
    def create_from_ui(self, orders):
        """Method to create booking order"""

        # import pdb; pdb.set_trace()
        list_order = self.env['dapur.order'].search([('state_dapur', '=', True)])
        cek_order = self._order_fields(orders)
        for list in list_order:
            exist = list.table_id.id == cek_order['table_id']
            if exist:
                #untuk menggantikan orderan yang sudah ada
                # update : unlink dulu terus add
                # problem : Kalau setiap item ada status (dimasak, selesai), nanti statusnya ilang


                # i.write({'lines': cek_order['lines']})
                # i.lines = self.write({'lines': cek_order['lines']})
                list.lines.unlink()
                list.lines = cek_order['lines']
                list_id = list.id
                list_name = list.name
                order = {'id': list_id,
                        'name': list_name}
                return order
                break
        if not exist:
            order_id = self.create(self._order_fields(orders))
            order = {'id': order_id.id,
                    'name': order_id.name}
            return order
                



        # order_id = self.create(self._order_fields(orders))
        # order = {'id': order_id.id,
        #          'name': order_id.name}
        # return order


    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('dapur.order') or '/'
        return super(dapur, self).create(vals)


class dapurLine(models.Model):
    _name = 'dapur.order.line'
    _rec_name = "product_id"



    def _order_line_fields(self, line):
        if line and 'tax_ids' not in line[2]:
            product = self.env['product.product'].browse(line[2]['product_id'])
            line[2]['tax_ids'] = [(6, 0, [x.id for x in product.taxes_id])]
        return line


    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    name = fields.Char(string='Line No')
    # notice = fields.Char(string='Discount Notice')
    product_id = fields.Many2one('product.product',
                                 string='Product',
                                 domain=[('sale_ok', '=', True)],
                                 required=True, change_default=True)
    # price_unit = fields.Float(string='Unit Price', digits=0)
    qty = fields.Float('Quantity', default=1)
    # price_subtotal = fields.Float(compute='_compute_amount_line_all',
    #                               digits=0,
    #                               string='Subtotal w/o Tax')
    # price_subtotal_incl = fields.Float(compute='_compute_amount_line_all',
    #                                    digits=0,
    #                                    string='Subtotal')
    # discount = fields.Float(string='Discount (%)', digits=0, default=0.0)
    order_id = fields.Many2one('dapur.order', string='Order Ref', ondelete='cascade')
    create_date = fields.Datetime(string='Creation Date', readonly=True)
    tax_ids = fields.Many2many('account.tax', string='Taxes', readonly=True)
    tax_ids_after_fiscal_position = fields.Many2many('account.tax', string='Taxes')
    pack_lot_ids = fields.One2many('pos.pack.operation.lot', 'pos_order_line_id',
                                   string='Lot/serial Number')
    
    state = fields.Selection([('waiting', 'Waiting'), ('on_progress', 'Dimasak'), ('done', 'Selesai')], 'Status Dapur')

