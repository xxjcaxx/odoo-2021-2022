# -*- coding: utf-8 -*-
# from odoo import http


# class Abp(http.Controller):
#     @http.route('/abp/abp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/abp/abp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('abp.listing', {
#             'root': '/abp/abp',
#             'objects': http.request.env['abp.abp'].search([]),
#         })

#     @http.route('/abp/abp/objects/<model("abp.abp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('abp.object', {
#             'object': obj
#         })
