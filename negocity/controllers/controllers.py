# -*- coding: utf-8 -*-
from odoo import http
import json
from odoo import tools

class banner_city_controller(http.Controller):
    @http.route('/negocity/city_banner', auth='user', type='json')
    def banner(self):
        return {
            'html': """
                <div  class="negocity_banner" style="height: 200px; background-size:100%; background-image: url(/negocity/static/src/img/negocity_city.jpg)">
                <div class="negocity_button" style="position: static; color:#fff;">
                <a class="banner_button" type="action" data-reload-on-close="true" 
                role="button" data-method="action_generate_cities" data-model="negocity.city">Generate Citiess</a>
                </div>
                </div> """
        }
# Podem resoldre el botó en un altre controller o amb una acció


    @http.route('/negocity/api/<model>', auth="none", cors='*', methods=["POST","PUT","OPTIONS"], csrf=False, type='json')
    def api(self, **args):
       print('APIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
       print(args, http.request.httprequest.method)
       model = args['model']
       if( http.request.httprequest.method == 'POST'):   #  {"jsonrpc":"2.0","method":"call","params":{"planet":{"name":"Trantor","average_temperature":20},"password":"1234"}}
           record = http.request.env['negocity.'+model].sudo().create(args[model])
           return record.read()
       if( http.request.httprequest.method == 'GET'):
           if 'id' in args:
               record = http.request.env['negocity.'+model].sudo().search([('id','=',args[model]['id'])])
           else:
               record = http.request.env['negocity.'+model].sudo().search([])
           return record.read()
       if( http.request.httprequest.method == 'PUT' or  http.request.httprequest.method == 'PATCH'):
           record = http.request.env['negocity.'+model].sudo().search([('id','=',args[model]['id'])])[0]
           record.write(args[model])
           return record.read()
       if(http.request.httprequest.method == 'DELETE'):
           record = http.request.env['negocity.'+model].sudo().search([('id','=',args[model]['id'])])[0]
           print(record)
           record.unlink()
           return record.read()

       return http.request.env['ir.http'].session_info()


    @http.route('/negocity/api/<model>', auth="none", cors='*', methods=["GET","DELETE"], csrf=False, type='http')
    def api(self, **args):
        print('APIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIGET')
        print(args, http.request.httprequest.method)
        model = args['model']
        if (http.request.httprequest.method == 'GET'):
            record = http.request.env['negocity.' + model].sudo().search([])
            #print(record.read())
            return http.Response(
            json.dumps(record.read(), default=tools.date_utils.json_default),
            status=200,
            mimetype='application/json'
           )
        if (http.request.httprequest.method == 'DELETE'):
            record = http.request.env['negocity.' + model].sudo().search([('id', '=', args[model]['id'])])[0]
            print(record)
            record.unlink()
            return http.Response(
                json.dumps(record.read()),
                status=200,
                mimetype='application/json'
            )

        return http.request.env['ir.http'].session_info()

#class Negocity(http.Controller):
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
