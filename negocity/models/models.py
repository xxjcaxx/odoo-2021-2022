# -*- coding: utf-8 -*-


from odoo import models, fields, api
import random
import math
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
## from odoo.exceptions import Warning   (Es considera obsolet en favor de UserError)
from odoo.exceptions import UserError


class building_type(models.Model):
    _name = 'negocity.building_type'
    _description = 'Building types'

    name = fields.Char()
    energy = fields.Float()  # Pot ser positiu o negatiu i aumenta en el nivell
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()
    despair = fields.Float(default=0)
    junk = fields.Float()  # Quantitat de junk que necessita i que proporciona
    time = fields.Float(compute='_get_time')  # En hores
    image = fields.Image(max_width=200, max_height=200)
    image_small = fields.Image(related='image', max_width=40, max_height=40,
                               string="image")  ###https://learnopenerp.blogspot.com/2021/09/dynamically-image-resizing-save-write-odoo14.html

    @api.depends('junk')
    def _get_time(self):
        for b in self:
            b.time = b.junk / 10


class building(models.Model):
    _name = 'negocity.building'
    _description = 'Buildings'

    name = fields.Char(related='type.name')
    type = fields.Many2one('negocity.building_type', ondelete='restrict')
    level = fields.Float(default=1)  # Possible widget
    ruined = fields.Float(default=50)  # 100% és ruina total i 0 està perfecte
    city = fields.Many2one('negocity.city', ondelete='cascade')

    junk_contributed = fields.Integer(default=0)
    junk_progress = fields.Float(compute='_get_junk_progress')
    workers = fields.Many2many('negocity.survivor', domain="[('id','in',workers_available)]")
    #workers = fields.Many2many('negocity.survivor', domain="[('city','=',city)]")
    workers_available = fields.Many2many('negocity.survivor',compute='_get_workers_available')
    time = fields.Float(compute='_get_time')
    date_start = fields.Datetime()
    date_end = fields.Datetime(compute='_get_time')
    progress = fields.Float()

    state = fields.Selection([('unfinished','Unfinished'),('inprogress','In Progress'),('finished','Finished')])

    # Coses del tipus
    image = fields.Image(related='type.image')
    energy = fields.Float(related='type.energy')  # Pot ser positiu o negatiu i aumenta en el nivell
    oil = fields.Float(related='type.oil')
    food = fields.Float(related='type.food')
    water = fields.Float(related='type.water')
    despair = fields.Float(related='type.despair')
    junk = fields.Float(related='type.junk')  # Quantitat de junk que necessita i que proporciona


    @api.depends('workers','city')
    def _get_workers_available(self):
        for b in self:
            b.workers_available = (b.city.survivors - b.workers).filtered(
                lambda w: len(w.city.buildings.workers.filtered(
                    lambda ww: ww.id == w.id))
                    ==0)

    @api.constrains('workers')
    def _check_workers(self):
        for b in self:
            for w in b.workers:
                if b.city.id != w.city.id:
                    raise ValidationError('The workers are not from the same city')

    @api.depends('junk_contributed')
    def _get_junk_progress(self):
        for b in self:
            contributed = b.junk_contributed
            expected = b.type.junk
            b.junk_progress = (contributed*100)/expected

    @api.depends('type', 'workers','date_start')
    def _get_time(self):  
        for b in self:
            if b.state != 'finished':
                # Primer traguem el temps total en la quantitat de treballadors actuals
                n_workers = len(b.workers)
                if n_workers > 0:
                    mean_illness = 0
                    for w in b.workers:
                        mean_illness = mean_illness + w.illnes
                    mean_illness = mean_illness / n_workers
                    b.time = b.type.time / math.log(n_workers * (100 - mean_illness),2)
                else:
                    b.time = b.type.time   
                remaining_percent = 100 - b.progress
                remaining_time = remaining_percent * b.time /100
                # treure data final
                if b.date_start:
                    b.date_end = fields.Datetime.to_string(fields.Datetime.from_string(fields.datetime.now()) + timedelta(hours=remaining_time))
                   # time_remaining =  fields.Datetime.context_timestamp(self,b.date_end) -  fields.Datetime.context_timestamp(self, datetime.now())
                else:
                    b.date_end = ''
            
            else:
                b.date_end = False
                b.time = 0


    @api.model
    def create(self,values):
        record = super(building, self).create(values)
        if record.junk_contributed >= record.type.junk and record.date_start == False:
          record.write({'date_start': fields.datetime.now(), 'state': 'inprogress'})
        return record


    def write(self,values):
         record = super(building, self).write(values)
         if self.junk_contributed >= self.type.junk and not self.date_start:
             self.write({'date_start': fields.datetime.now(),'state':'inprogress'})
         return record


    @api.model
    def update_building(self):
        buildings_in_progress = self.search([('state','=','inprogress')])
        print("Updating progress in: ",buildings_in_progress)
        for b in buildings_in_progress:
            percent_in_a_minute = 100 / (b.time*60)
            b.write({'progress':b.progress+percent_in_a_minute})
            if b.progress >= 100:
                b.write({'progress':100,'state':'finished','workers':[(5,0,0)],'ruined':0})   # Desvincule sense eliminar als treballadors
                


class survivor(models.Model):
    _name = 'negocity.survivor'
    _description = 'Survivors'

    def _generate_name(self):
        first = ["Commander", "Bullet", "Imperator", "Doof", "Duff", "Immortal", "Big", "Grease", "Junk", "Rusty"
                                                                                                          "Gas", "War",
                 "Feral", "Blood", "Lead", "Max", "Sprog", "Allan", "Smoke", "Wagon", "Baron", "Leather", "Rotten"
                                                                                                          "Salt",
                 "Slake", "Sick", "Sickly", "Nuke", "Oil", "Night", "Water", "Tank", "Rig", "People", "Nocturne",
                 "Satanic"
                 "Dead", "Wandering", "Suffering", "Unfit", "Deadly", "Mike", "Nomad", "Mad", "Jhonny", "Unpredictable",
                 "Freakish", "Snake", "Praying"]
        second = ["Killer", "Rider", "Cutter", "Guts", "Eater", "Warrior", "Colossus", "Blaster", "Gunner", "Smith",
                  "Doe"
                  "Farmer", "Rock", "Claw", "Boy", "Girl", "Driver", "Ace", "Quick", "Blitzer", "Fury", "Roadster",
                  "Interceptor", "Bastich", "Dweller", "Thief", "Bleeder", "Face", "Mutant", "Anomaly", "Risk",
                  "Garcia", "Salamanca", "Goodman", "Sakura", "Bleding Gums", "Absent", "Hybrid", "Desire", "Bubblegum"
            , "Serpente", "Petal", "Dust", "Mantis", "Preacher", "Harkonnen", "Heisenberg", "Vonn Newman"]
        return random.choice(first) + " " + random.choice(second)

    name = fields.Char(default=_generate_name)
    desperation = fields.Float(default=50)
    mutations = fields.Float(default=1)
    illnes = fields.Float(default=1)
    template = fields.Many2one('negocity.character_template', ondelete='restrict')
    avatar = fields.Image(max_width=200, max_height=400, related='template.image')

    city = fields.Many2one('negocity.city', ondelete='restrict')
    player = fields.Many2one('negocity.player', ondelete='set null')
    vehicles = fields.One2many('negocity.vehicle', 'survivor')

    junk = fields.Integer(default=0)
    building = fields.Many2many('negocity.building')

    travel = fields.Many2one('negocity.travel')


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

    
    def launch_travel(self):
        for t in self:
            if t.oil_available >= t.oil_required:
                t.date_departure = fields.datetime.now()
                t.vehicle.city = False
                t.driver.city = False
                t.driver.travel = t.id
                for p in t.passengers:
                    p.city = False
                t.state = 'inprogress'
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

    ### Opció de reparar edificis o convertir-los en junk
    ### Opció de donar gasolina a la ciutat
    ### Veure en una cituat els viatges que estan vinguent
    ### Les batalles es faran creuant dos viatges. Quan un player envia un viatge pot ser per anar a furtar a una ciutat o per a defendrer-la.
    ###     Un player o molts poden enviar molts viatges, com que van per la carretera, els que vinguen en direcció contraria lluitaran.
    ####    Les restes de la lluita (chatarra i gasolina) es queden en la carretera fins a que passe algú
    ### Producció dels edificis
    ### Salud i progressió dels supervivents