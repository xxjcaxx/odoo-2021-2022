# -*- coding: utf-8 -*-
from odoo import http
import json
from odoo import tools


class Proves_controller(http.Controller):
     @http.route('/proves/productes/', auth="none", cors='*', csrf=False, type='http')
     def get_productes(self, **kw):
         productes = http.request.env['product.product'].sudo().search([])
         print(productes)
        # return json.dumps(productes.read(['id','name','image_1920']))

         return http.Response(
            json.dumps(productes.read(['id','name','image_1920']), default=tools.date_utils.json_default),
            status=200,
            mimetype='application/json'
           )

     @http.route('/proves/comandes/', auth="none", cors='*', methods=["POST"], csrf=False,
                 type='json')
     def comandespost(self, **args):
         print('APIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
         print(args, http.request.httprequest.method)

         if (http.request.httprequest.method == 'POST'):
             print('POST')
             record = http.request.env['pos.order'].sudo().create_from_ui([args], True)


         return http.request.env['ir.http'].session_info()

#     @http.route('/proves/proves/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('proves.listing', {
#             'root': '/proves/proves',
#             'objects': http.request.env['proves.proves'].search([]),
#         })

#     @http.route('/proves/proves/objects/<model("proves.proves"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proves.object', {
#             'object': obj
#         })
