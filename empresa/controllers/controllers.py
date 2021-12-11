# -*- coding: utf-8 -*-
# from odoo import http


# class Empresa(http.Controller):
#     @http.route('/empresa/empresa/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/empresa/empresa/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('empresa.listing', {
#             'root': '/empresa/empresa',
#             'objects': http.request.env['empresa.empresa'].search([]),
#         })

#     @http.route('/empresa/empresa/objects/<model("empresa.empresa"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('empresa.object', {
#             'object': obj
#         })
