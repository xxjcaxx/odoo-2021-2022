# -*- coding: utf-8 -*-
from odoo import http


class pedidos(http.Controller):
 #    @http.route('/school/pedidos/', auth='public')
 #    def pedidos(self, **kw):
#         return "Hello, world"
     @http.route('/school/pedidos', auth='public', cors='*', type='json')
     def pedidos(self, name, **kw):
        school = http.request.env['school.school'].sudo().create({'name':name})
        print('rghghhhhhhhhhhhhhhhhhhhh')
        return school.read()[0]
#     @http.route('/school/school/objects/<model("school.school"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school.object', {
#             'object': obj
#         })
