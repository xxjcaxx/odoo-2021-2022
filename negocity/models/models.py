# -*- coding: utf-8 -*-


from odoo import models, fields, api
import random
import math
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
## from odoo.exceptions import Warning   (Es considera obsolet en favor de UserError)
from odoo.exceptions import UserError




class vehicle(models.Model):
    _name = 'negocity.vehicle'
    _description = 'vehicles'
    name = fields.Char()
   # type = fields.Selection([('truck','Truck'),('car','Car'),('bus','Bus')])
    oil_consumption = fields.Float()
    gas_tank = fields.Float()
    gas_tank_level = fields.Float(default=0)
    speed = fields.Float()
    passengers = fields.Integer()
    junk_level = fields.Float()
    damage = fields.Float()     # Un turisme 10, un camió armat 10000 per fer-se una idea
    resistence = fields.Float()
    survivor = fields.Many2one('negocity.survivor')
    city = fields.Many2one('negocity.city')
    template = fields.Many2one('negocity.vehicle_template')
    img = fields.Image(max_width=400, max_height=200, string="Image")
    img_computed = fields.Image(compute='_get_img')



    def _get_img(self):
        for v in self:
            if v.img != False:
                v.img_computed = v.img
            else:
                v.img_computed = v.template.image

    def fill_gas_tank(self):
        for v in self:
            gas_available = v.city.oil
            if gas_available > v.gas_tank:
                v.gas_tank_level = v.gas_tank
                v.city.oil = gas_available - v.gas_tank_level
            else:
                v.gas_tank_level = v.city.oil
                v.city.oil = 0

    def donate_gas_tank(self):
        for v in self:
            v.city.oil =   v.city.oil + v.gas_tank_level
            v.gas_tank_level = 0
            


class event(models.Model):
    _name = 'negocity.event'
    _description = 'Events'

    name = fields.Char()
    player = fields.Many2many('negocity.player')
    event = fields.Reference([('negocity.building','Building'),('negocity.travel','Travel'),('negocity.collision','Collision'),('negocity.player','Player'),('negocity.survivor','Survivor')])
    description = fields.Text()

    @api.model
    def clean_messages(self):
        yesterday = fields.Datetime.to_string(datetime.now()-timedelta(hours=24))
        old_messages = self.search([('creation_date','<',yesterday)])
        old_messages.unlink()



    ### TODO

    ### 
    ### Opció de donar gasolina i junk a la ciutat
    ### Veure en una cituat els viatges que estan vinguent
    ### Les batalles es faran creuant dos viatges. Quan un player envia un viatge pot ser per anar a furtar a una ciutat o per a defendrer-la.
    ###     Un player o molts poden enviar molts viatges, com que van per la carretera, els que vinguen en direcció contraria lluitaran.
    ####    Les restes de la lluita (chatarra i gasolina) es queden en la carretera fins a que passe algú
    ### Producció dels edificis
    ### Salud i progressió dels supervivents
    ### Salud dels vehicles


    ### Wizards:  Create building , cReate travel, generate full game