# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random

class city(models.Model):
    _name = 'negocity.city'

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
    despair = fields.Float(default=50)
    radiation = fields.Float(default=50)

    buildings = fields.One2many('negocity.building','city')

class building_type(models.Model):
    _name = 'negocity.building_type'

    name = fields.Char()
    energy = fields.Float() # Pot ser positiu o negatiu i aumenta en el nivell
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()
    despair = fields.Float(default=0)

class building(models.Model):
    _name = 'negocity.building'

    name = fields.Char()
    type = fields.Many2one('negocity.building_type')
    level = fields.Float(default=1) # Possible widget
    ruined = fields.Float(default=50) # 100% és ruina total i 0 està perfecte
    city = fields.Many2one('negocity.city')


class survivor(models.Model):
    _name = 'negocity.survivor'
    def _generate_name(self):
        first = ["Commander","Bullet","Imperator","Doof","Duff","Immortal","Big","Grease", "Junk", "Rusty"
                 "Gas","War","Feral","Blood","Lead","Max","Sprog","Smoke","Wagon","Baron", "Leather", "Rotten"
                 "Salt","Slake","Nuke","Oil","Night","Water","Tank","Rig","People","Nocturne",
                 "Dead", "Deadly", "Mike", "Mad", "Jhonny"]
        second = ["Killer","Rider","Cutter","Guts","Eater","Warrior","Colossus","Blaster","Gunner", "Smith", "Doe"
                  "Farmer","Rock","Claw", "Boy", "Girl", "Driver","Ace","Quick","Blitzer", "Fury", "Roadster",
                  "Interceptor", "Bastich", "Thief", "Bleeder", "Face", "Mutant", "Anomaly", "Risk",
                  "Garcia", "Salamanca", "Goodman", "Sakura"]
        return random.choice(first)+" "+random.choice(second)

    name = fields.Char(default=_generate_name)
    desperation = fields.Float(default=50)
    mutations = fields.Float(default=1)
    illnes = fields.Float(default=1)

    city = fields.Many2one('negocity.city')

class vehicle(models.Model):
    _name = 'negocity.vehicle'

    name = fields.Char()
    oil_consumption = fields.Float()
    gas_tank = fields.Float()
    passengers = fields.Integer()
    junk_level = fields.Float()
    damage = fields.Float()

    survivor = fields.Many2one('negocity.survivor')