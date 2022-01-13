# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import math
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    is_premium = fields.Boolean()
    date_end = fields.Datetime()


class travel_premium(models.Model):
    _name = 'negocity.travel'
    _inherit = 'negocity.travel'

    @api.model
    def get_time(self, vehicle_id, road_id):
        time = super(travel_premium,self).get_time(vehicle_id,road_id)
        if (self.env['negocity.vehicle'].browse(vehicle_id).survivor.player.is_premium == True):
            time = time/2
            print(time)
        else:
            print(time,self.env['negocity.vehicle'].browse(vehicle_id).survivor.player.name)
        return time

class product_premium(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    is_premium = fields.Boolean(default=False)
    days_premium = fields.Integer()

class sale_premium(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'


    def apply_premium(self):

        premium_products = self.order_lines

        sale_date = self.date_order
        now = fields.Datetime.now()


        print(self)

    def write(self,values):
        super(sale_premium,self).write(values)
        self.apply_premium()

    @api.model
    def create(self,values):
        record = super(sale_premium,self).create(values)
        record.apply_premium()