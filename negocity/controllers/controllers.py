# -*- coding: utf-8 -*-
# from odoo import http


# class Negocity(http.Controller):
#     @http.route('/negocity/negocity/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/negocity/negocity/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('negocity.listing', {
#             'root': '/negocity/negocity',
#             'objects': http.request.env['negocity.negocity'].search([]),
#         })

#     @http.route('/negocity/negocity/objects/<model("negocity.negocity"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('negocity.object', {
#             'object': obj
#         })
