# -*- coding: utf-8 -*-
from odoo import http

# class PilihMenu(http.Controller):
#     @http.route('/pilih_menu/pilih_menu/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pilih_menu/pilih_menu/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pilih_menu.listing', {
#             'root': '/pilih_menu/pilih_menu',
#             'objects': http.request.env['pilih_menu.pilih_menu'].search([]),
#         })

#     @http.route('/pilih_menu/pilih_menu/objects/<model("pilih_menu.pilih_menu"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pilih_menu.object', {
#             'object': obj
#         })