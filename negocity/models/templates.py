# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import math
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError




class character_template(models.Model):
    _name = 'negocity.character_template'
    _description = 'Templates to generate characters'
    name = fields.Char()
    image = fields.Image(max_width=200, max_height=400)

class vehicle_template(models.Model):
    _name = 'negocity.vehicle_template'
    _description = 'Templates to generate vehicles'
    name = fields.Char()
    image = fields.Image(max_width=200, max_height=400)
    oil_consumption = fields.Float()
    gas_tank = fields.Float()
    speed = fields.Float()
    passengers = fields.Integer()
    damage = fields.Float()     # Un turisme 10, un camió armat 10000 per fer-se una idea

    score = fields.Float(compute='_get_score')
    score_stored = fields.Float()

    def _get_score(self):
        for v in self:
            v.score = -v.oil_consumption + (v.gas_tank / 100 )+ (v.speed / 10 ) + (v.passengers /5 ) + v.damage / 100
            if v.score >= 99:
                v.score = 99
            v.score_stored = v.score


    def get_random_vehicle(self):
        all_population = []
        for c in self.search([]):
            population = 100 - c.score
            for i in range(0, round(population)):
                all_population.append(c.id)
       # print(all_population)
        print(self.browse(random.choice(all_population)).mapped(lambda c: c.name+" "+str(c.score)))
        return self.browse(random.choice(all_population))
