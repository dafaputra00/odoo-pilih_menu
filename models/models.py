
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
            'state_dapur': ui_order['state_dapur'] or '',
            'pos_reference': ui_order['name'],
        }


    name = fields.Char(string='Dapur Ref', required=True, readonly=True, copy=False, default='/')
    pos_reference = fields.Char(string='Receipt Ref', readonly=True, copy=False)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)
    date_quotation = fields.Datetime(string='Quotation Date',
                                     readonly=True, index=True, default=fields.Datetime.now)
    lines = fields.One2many('dapur.order.line', 'order_id', string='Order Lines', copy=True)
    table_id = fields.Many2one('restaurant.table', string='Table', help='The table where this order was served')
    state = fields.Selection([('draft', 'New'), ('done', 'Done')],
                             'Status', readonly=True, copy=False, default='draft')
    dapur_order_ref = fields.Char(string='Booked Order Ref', readonly=True, copy=False)
    state_dapur = fields.Boolean('Kirim ke dapur', readonly=True)

    @api.model
    def ubahState(self, order_ref):
        import pdb; pdb.set_trace()
        list_order = self.env['dapur.order'].search([('state_dapur', '=', True)])
        for list in list_order:
            if(order_ref == list.pos_reference):
                list.state_dapur = False
                break

    @api.model
    def create_from_ui(self, orders):
        """Method to create booking order"""

        # python debugging
        # import pdb; pdb.set_trace() 
        
        list_order = self.env['dapur.order'].search([('state_dapur', '=', True)])
        cek_order = self._order_fields(orders)
        exist = False
        for list in list_order:
            exist = list.pos_reference == cek_order['pos_reference']
            if exist:
                #untuk menggantikan orderan yang sudah ada
                # update : unlink dulu terus add
                # problem : Kalau setiap item ada status (dimasak, selesai), nanti statusnya ilang
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
    product_id = fields.Many2one('product.product',
                                 string='Product',
                                 domain=[('sale_ok', '=', True)],
                                 required=True, change_default=True)
    qty = fields.Float('Quantity', default=1)
    order_id = fields.Many2one('dapur.order', string='Order Ref', ondelete='cascade')
    create_date = fields.Datetime(string='Creation Date', readonly=True)
    tax_ids = fields.Many2many('account.tax', string='Taxes', readonly=True)
    tax_ids_after_fiscal_position = fields.Many2many('account.tax', string='Taxes')
    pack_lot_ids = fields.One2many('pos.pack.operation.lot', 'pos_order_line_id',
                                   string='Lot/serial Number')
    
    state = fields.Selection([('waiting', 'Waiting'), ('on_progress', 'Dimasak'), ('done', 'Selesai')], 'Status Dapur')

