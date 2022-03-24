# -*- coding: utf-8 -*-
# from odoo import http


# class Pcfutbol(http.Controller):
#     @http.route('/pcfutbol/pcfutbol/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pcfutbol/pcfutbol/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pcfutbol.listing', {
#             'root': '/pcfutbol/pcfutbol',
#             'objects': http.request.env['pcfutbol.pcfutbol'].search([]),
#         })

#     @http.route('/pcfutbol/pcfutbol/objects/<model("pcfutbol.pcfutbol"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pcfutbol.object', {
#             'object': obj
#         })
