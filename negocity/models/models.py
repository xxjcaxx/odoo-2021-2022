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
            

class road(models.Model):
    _name = 'negocity.road'
    _description = 'Road beween cities'

    name = fields.Char(compute='_get_name')
    city_1 = fields.Many2one('negocity.city', ondelete='cascade')
    city_2 = fields.Many2one('negocity.city', ondelete='cascade')
    distance = fields.Float(compute='_get_distance')

    @api.depends('city_1','city_2')
    def _get_name(self):
        for r in self:
            r.name = r.city_1.name+" <--> "+r.city_2.name

    @api.depends('city_1','city_2')
    def _get_distance(self):
        for r in self:
            r.distance = math.sqrt((r.city_2.position_x - r.city_1.position_x)**2 + (r.city_2.position_y - r.city_1.position_y)**2)
          #  print(r.distance)


class travel(models.Model):
    _name = 'negocity.travel'
    _description = 'Travels'

    name = fields.Char()
    origin = fields.Many2one('negocity.city', ondelete='cascade')
    destiny = fields.Many2one('negocity.city', ondelete='cascade')  # filtrat
    road = fields.Many2one('negocity.road', ondelete='cascade')  # computat
    date_departure = fields.Datetime()
    date_end = fields.Datetime(compute='_get_progress')  # sera computat en funció de la distància
    progress = fields.Float(compute='_get_progress')
    state = fields.Selection([('preparation','Preparation'),('inprogress','In Progress'),('finished','Finished')],default='preparation')


    player = fields.Many2one('negocity.player')
    passengers = fields.Many2many('negocity.survivor')  # filtrats sols els que són de la ciutat origin i del player
    driver = fields.Many2one('negocity.survivor')
    vehicle = fields.Many2one('negocity.vehicle')
    oil_required = fields.Float(compute='_get_progress')
    oil_available = fields.Float(related='vehicle.gas_tank_level')


    @api.constrains('origin','destiny','road','player','passengers','driver','vehicle')
    def check_things(self):
        for t in self:
            if t.origin.id != t.road.city_1.id and t.origin.id != t.road.city_2.id or  t.destiny.id != t.road.city_1.id and t.destiny.id != t.road.city_2.id  :
                raise ValidationError('Incorrect Road')
            if t.driver.city.id != t.origin.id:
                raise ValidationError('Driver has to be in origin city')
            for p in t.passengers:
                if p.city.id != t.origin.id:
                    raise ValidationError('Passengers has to be in origin city')
            if t.vehicle.city != t.city.id:
                raise ValidationError('Vehicle has to be in origin city')
            if t.driver.player.id != t.player.id:
                raise ValidationError('Driver has to be in player')
            for p in t.passengers:
                if p.player.id != t.player.id:
                    raise ValidationError('Passengers has to be in player')

    def launch_travel(self):
        for t in self:
            if t.oil_available >= t.oil_required:
                if t.vehicle.junk_level < 100:
                    t.date_departure = fields.datetime.now()
                    t.vehicle.city = False
                    t.driver.city = False
                    t.driver.travel = t.id
                    for p in t.passengers:
                        p.city = False
                    t.state = 'inprogress'
                else:
                     raise UserError('Vehicle is not ready')
            else:
                raise UserError('Not Sufficient Oil for the travel')

    @api.onchange('origin')
    def _onchange_origin(self):
        if self.origin != False:
            roads_available =  self.origin.roads   #  self.env['negocity.road'].search(['|',('city_1','=', self.origin.id),('city_2','=', self.origin.id)])
            cities_available = roads_available.city_1 + roads_available.city_2 - self.origin
            players_in_city = self.origin.players.ids
            print(cities_available)
            return {
                'domain' : {
                    'destiny': [('id', 'in', cities_available.ids)], 
                    'player': [('id','in',players_in_city)]
                }
            }
    
    @api.onchange('destiny')
    def _onchange_destiny(self):
        if self.destiny != False:
            road_available = self.origin.roads & self.destiny.roads
            self.road = road_available.id
            return {}

    @api.onchange('player')
    def _onchange_player(self):
        if self.player != False:
            drivers_available = self.player.survivors.filtered(lambda s: s.city.id == self.origin.id and len(s.building) == 0 )
            return {
                'domain' : {
                    'driver': [('id', 'in', drivers_available.ids)],
                    'passengers': [('id','in',drivers_available.ids)]
                }
            }

    @api.onchange('driver')
    def _onchange_driver(self):
        if self.driver != False:
            vehicles = self.driver.vehicles
            return {
                'domain' : {
                    'vehicle': [('id', 'in', vehicles.ids)]
                }
            }
    
    
    @api.depends('date_departure','road','vehicle')
    def _get_progress(self):
        for t in self:
            if t.road and t.vehicle:
                time = t.road.distance  # En hores si va a 60k/h
                distance = time * 60
                time = distance / t.vehicle.speed  # 
                if time <= 0:
                    time = 0.01
                t.oil_required = (distance/100) * t.vehicle.oil_consumption
                print(distance,t.vehicle.speed,time,t.oil_required)
                if t.date_departure:
                        d_dep = t.date_departure
                        data = fields.Datetime.from_string(d_dep)
                        data = data + timedelta(hours=time)
                        t.date_end = fields.Datetime.to_string(data)
                        time_remaining =  fields.Datetime.context_timestamp(self,t.date_end) -  fields.Datetime.context_timestamp(self, datetime.now())
                        time_remaining = time_remaining.total_seconds()/60/60
                        t.progress =  (1 - time_remaining / time)*100 
                        if t.progress >= 100:
                            t.progress = 100
                else:
                    t.progress = 0
                    t.date_end = False
                
            else:
                t.progress = 0
                t.date_end = False
                t.oil_required = 0 


    @api.model
    def update_travel(self):
        travels_in_progress = self.search([('state','=','inprogress')])
        print("Updating progress in: ",travels_in_progress)
        for t in travels_in_progress:
            if t.progress >= 100:
                t.write({'state':'finished'})   

################  FALTA ELS PROBLEMES EN EL TRAVEL


                t.driver.write({'city':t.destiny.id})
                t.vehicle.write({'city':t.destiny.id,'gas_tank_level':t.vehicle.gas_tank_level-t.oil_required})
                for p in t.passengers:
                    p.write({'city':t.destiny.id})
                self.env['negocity.event'].create({'name':'Arrival travel '+t.name, 'player':t.player, 'event':'negocity.travel,'+str(t.id), 'description': 'Arrival travel... '})
                print('Arribal')




class event(models.Model):
    _name = 'negocity.event'
    _description = 'Events'

    name = fields.Char()
    player = fields.Many2many('negocity.player')
    event = fields.Reference([('negocity.building','Building'),('negocity.travel','Travel')])
    description = fields.Text()





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