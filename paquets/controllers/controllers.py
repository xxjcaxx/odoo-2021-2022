# -*- coding: utf-8 -*-
# from odoo import http


# class Paquets(http.Controller):
#     @http.route('/paquets/paquets/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/paquets/paquets/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('paquets.listing', {
#             'root': '/paquets/paquets',
#             'objects': http.request.env['paquets.paquets'].search([]),
#         })

#     @http.route('/paquets/paquets/objects/<model("paquets.paquets"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('paquets.object', {
#             'object': obj
#         })
