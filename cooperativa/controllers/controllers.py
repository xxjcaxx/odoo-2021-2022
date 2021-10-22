# -*- coding: utf-8 -*-
# from odoo import http


# class Cooperativa(http.Controller):
#     @http.route('/cooperativa/cooperativa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cooperativa/cooperativa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cooperativa.listing', {
#             'root': '/cooperativa/cooperativa',
#             'objects': http.request.env['cooperativa.cooperativa'].search([]),
#         })

#     @http.route('/cooperativa/cooperativa/objects/<model("cooperativa.cooperativa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cooperativa.object', {
#             'object': obj
#         })
