# -*- coding: utf-8 -*-

from operator import pos
from odoo import models, fields, api
import random
import math

class player(models.Model):
    _name = 'negocity.player'
    _description = 'Players'

    name = fields.Char()
    survivors = fields.One2many('negocity.survivor','player')

class city(models.Model):
    _name = 'negocity.city'
    _description = 'Cities'

    def _generate_name(self):
        first = ["Uncanny","Remote","Eastern","Dead","Whispering", "Unfriendly", "Unpleasant", "Nasty"
        "Darkest","Broken","Rotten","Sunny","Dead","Wild","Forgotten","Distressing", "Unlikeable", "Rough",
        "Hard", "Sharp", "Thug", "Bully", "Disruptive", "Oily", "Burned", "Sunken", "Hollow"
        "Burning","Frozen","Sad","Big","Creepy","Desolate","Polluted","Fecal","Infected","Tainted"]
        second = ["Tundra","Badlands","Flatlands","Desert","Flat","Paramo","Desierto",
         "Dunghill","Sands","Rocks","Dry Land","Borderlands","Frontier", "Ruins",
         "Cliff","Junk","Crater","City","Suburbs","Underground","Dump","Graveyard","Plain","Debris"]
        return random.choice(first)+" "+random.choice(second)

    name = fields.Char(default=_generate_name)


    energy = fields.Float()   
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()
    despair = fields.Float(default=50) # % 
    radiation = fields.Float(default=50)  # %

    buildings = fields.One2many('negocity.building','city')
    survivors = fields.One2many('negocity.survivor','city')

    position_x = fields.Integer()
    position_y = fields.Integer()

    @api.model
    def action_generate_cities(self):
        print('**************Generate')
        existent_cities = self.search([])
        existent_cities.unlink()
        board = [[0 for x in range(50)] for y in range(50)]
        new_cities = self
     
        if len(existent_cities) != -1:
            positions = [x for x in range(2500)] 
            random.shuffle(positions)
            #print(positions)
            for i in range(0,50):
                x = math.floor(positions[i]/50)
                y = positions[i]%50
                print(x,y)
                board[x][y]=1
                new_city = self.create({
                    "energy": random.random()*100, 
                    "oil": random.random()*100, 
                    "food": random.random()*100, 
                    "water": random.random()*100,
                    "radiation": random.random()*100,
                    "position_x": x,
                    "position_y": y })
                new_cities = new_cities | new_city
            #for i in range(50):
            #    print(board[i])

            # Crear les carreteres
            #cities_done = self
            #for c in new_cities:
            #    cities_done = cities_done | c
            #    for c2 in new_cities - cities_done:
            #        self.env['negocity.road'].create({'city_1': c.id, 'city_2': c2.id})

            all_roads = False
            i = 1
            while all_roads == False:
                all_roads = True
                
                for c in new_cities:
                    distancias = new_cities.sorted(key=lambda r: math.sqrt(
                        (r.position_x-c.position_x)**2
                        +(r.position_y-c.position_y)**2) 
                        )
                    # Si no exiteix previament una igual
                    if len(distancias) > i:
                     # print('i:',i)
                      if (len(self.env['negocity.road'].search([('city_1','=', distancias[i].id),('city_2','=', c.id)])) == 0):  
                      # print(self.env['negocity.road'].search([('city_2','=', distancias[i].id),('city_1','=', c.id)]))
                       if (len(self.env['negocity.road'].search([('city_2','=', distancias[i].id),('city_1','=', c.id)])) == 0 ):
                       # print('Mateixa',c.id)
                        # Si no té colisió
                        # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
                        def ccw(A,B,C):
                            return (C.position_y-A.position_y) * (B.position_x-A.position_x) > (B.position_y-A.position_y) * (C.position_x-A.position_x)
                        # Return true if line segments AB and CD intersect
                        def intersect(A,B,C,D):
                            return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
                        colisionen = self.env['negocity.road'].search([]).filtered(lambda r: intersect(r.city_1,r.city_2,c,distancias[i]))
                        if len(colisionen) == 0:
                            self.env['negocity.road'].create({'city_1': c.id, 'city_2': distancias[i].id})  # la primera és ella mateixa
                            all_roads = False
                i = i+1
                print(all_roads,i)


class building_type(models.Model):
    _name = 'negocity.building_type'
    _description = 'Building types'

    name = fields.Char()
    energy = fields.Float() # Pot ser positiu o negatiu i aumenta en el nivell
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()
    despair = fields.Float(default=0)

class building(models.Model):
    _name = 'negocity.building'
    _description = 'Buildings'

    name = fields.Char()
    type = fields.Many2one('negocity.building_type')
    level = fields.Float(default=1) # Possible widget
    ruined = fields.Float(default=50) # 100% és ruina total i 0 està perfecte
    city = fields.Many2one('negocity.city')


class survivor(models.Model):
    _name = 'negocity.survivor'
    _description = 'Survivors'

    def _generate_name(self):
        first = ["Commander","Bullet","Imperator","Doof","Duff","Immortal","Big","Grease", "Junk", "Rusty"
                 "Gas","War","Feral","Blood","Lead","Max","Sprog","Smoke","Wagon","Baron", "Leather", "Rotten"
                 "Salt","Slake","Nuke","Oil","Night","Water","Tank","Rig","People","Nocturne", "Satanic"
                 "Dead", "Deadly", "Mike", "Mad", "Jhonny","Unpredictable","Freakish","Snake","Praying"]
        second = ["Killer","Rider","Cutter","Guts","Eater","Warrior","Colossus","Blaster","Gunner", "Smith", "Doe"
                  "Farmer","Rock","Claw", "Boy", "Girl", "Driver","Ace","Quick","Blitzer", "Fury", "Roadster",
                  "Interceptor", "Bastich", "Thief", "Bleeder", "Face", "Mutant", "Anomaly", "Risk",
                  "Garcia", "Salamanca", "Goodman", "Sakura","Bleding Gums","Absent","Hybrid","Desire","Bubblegum"
                  ,"Serpente","Petal","Dust","Mantis","Preacher"]
        return random.choice(first)+" "+random.choice(second)

    name = fields.Char(default=_generate_name)
    desperation = fields.Float(default=50)
    mutations = fields.Float(default=1)
    illnes = fields.Float(default=1)

    city = fields.Many2one('negocity.city')
    player = fields.Many2one('negocity.player')

class vehicle(models.Model):
    _name = 'negocity.vehicle'
    _description = 'vehicles'
    name = fields.Char()
    oil_consumption = fields.Float()
    gas_tank = fields.Float()
    passengers = fields.Integer()
    junk_level = fields.Float()
    damage = fields.Float()

    survivor = fields.Many2one('negocity.survivor')

class road(models.Model):
    _name = 'negocity.road'
    _description = 'Road beween cities'

    city_1 = fields.Many2one('negocity.city', ondelete='cascade')
    city_2 = fields.Many2one('negocity.city', ondelete='cascade')