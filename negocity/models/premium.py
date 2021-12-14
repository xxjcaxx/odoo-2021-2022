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