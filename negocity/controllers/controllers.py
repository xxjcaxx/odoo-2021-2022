# -*- coding: utf-8 -*-
from odoo import http


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
