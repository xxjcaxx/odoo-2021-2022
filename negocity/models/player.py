# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import math
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class player(models.Model):
    _name = 'negocity.player'
    _description = 'Players'

    name = fields.Char()
    avatar = fields.Image(max_width=200, max_height=200)
    avatar_icon = fields.Image(related='avatar', max_width=50,
                               max_height=50)  ###https://learnopenerp.blogspot.com/2021/09/dynamically-image-resizing-save-write-odoo14.html
    survivors = fields.One2many('negocity.survivor', 'player')
    survivors_tree = fields.One2many('negocity.survivor', related = 'survivors')
    quantity_survivors = fields.Integer(compute='_get_q_survivors')
    registration_date = fields.Datetime()
    cities = fields.Many2many('negocity.city',compute='_get_cities')
    buildings = fields.Many2many('negocity.building',compute='_get_cities')
    vehicles = fields.Many2many('negocity.vehicle',compute='_get_cities')
    login = fields.Char()
    password = fields.Char()
    events = fields.One2many('negocity.event','player')

    @api.depends('survivors')
    def _get_q_survivors(self):
        for p in self:
            p.quantity_survivors = len(p.survivors)

    def create_survivor(self):
        for p in self:
            template = random.choice(self.env['negocity.character_template'].search([]).mapped(lambda t: t.id))
            city = random.choice(self.env['negocity.city'].search([]).mapped(lambda t: t.id))
            survivor = self.env['negocity.survivor'].create({'player': p.id, 'template': template, 'city': city})
            for i in range(0,random.randint(0,1)):
                survivor.assign_random_car()



    @api.depends('survivors')
    def _get_cities(self):
        for p in self:
            p.cities = p.survivors.city.ids   # Funciona perque son recordsets
            p.buildings = p.cities.buildings.filtered(lambda b: b.progress < 100)
            p.vehicles = p.survivors.vehicles.ids
           #p.cities = []
          #  p.buildings = []

    def update_survivors(self):
            self.env['negocity.survivor'].update_survivor()