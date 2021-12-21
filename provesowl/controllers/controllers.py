# -*- coding: utf-8 -*-
# from odoo import http


# class Provesowl(http.Controller):
#     @http.route('/provesowl/provesowl', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/provesowl/provesowl/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('provesowl.listing', {
#             'root': '/provesowl/provesowl',
#             'objects': http.request.env['provesowl.provesowl'].search([]),
#         })

#     @http.route('/provesowl/provesowl/objects/<model("provesowl.provesowl"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('provesowl.object', {
#             'object': obj
#         })
