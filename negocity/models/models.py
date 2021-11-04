# -*- coding: utf-8 -*-

from operator import pos
from odoo import models, fields, api
import random
import math
from datetime import datetime, timedelta


class player(models.Model):
    _name = 'negocity.player'
    _description = 'Players'

    name = fields.Char()
    avatar = fields.Image(max_width=200, max_height=200)
    avatar_icon = fields.Image(related='avatar', max_width=50,
                               max_height=50)  ###https://learnopenerp.blogspot.com/2021/09/dynamically-image-resizing-save-write-odoo14.html
    survivors = fields.One2many('negocity.survivor', 'player')
    quantity_survivors = fields.Integer(compute='_get_q_survivors')
    registration_date = fields.Datetime()

    @api.depends('survivors')
    def _get_q_survivors(self):
        for p in self:
            p.quantity_survivors = len(p.survivors)

    def create_survivor(self):
        for p in self:
            template = random.choice(self.env['negocity.character_template'].search([]).mapped(lambda t: t.id))
            city = random.choice(self.env['negocity.city'].search([]).mapped(lambda t: t.id))
            self.env['negocity.survivor'].create({'player': p.id, 'template': template, 'city': city})


class city(models.Model):
    _name = 'negocity.city'
    _description = 'Cities'

    def _generate_name(self):
        first = ["Uncanny", "Remote", "Eastern", "Dead", "Whispering", "Unfriendly", "Unpleasant", "Nasty"
                                                                                                   "Darkest", "Broken",
                 "Rotten", "Sunny", "Dead", "Wild", "Forgotten", "Distressing", "Unlikeable", "Rough",
                 "Hard", "Sharp", "Thug", "Bully", "Disruptive", "Oily", "Burned", "Sunken", "Hollow"
                                                                                             "Burning", "Frozen", "Sad",
                 "Big", "Creepy", "Desolate", "Polluted", "Fecal", "Infected", "Tainted"]
        second = ["Tundra", "Badlands", "Flatlands", "Desert", "Flat", "Paramo", "Desierto",
                  "Dunghill", "Sands", "Rocks", "Dry Land", "Borderlands", "Frontier", "Ruins",
                  "Cliff", "Junk", "Crater", "City", "Suburbs", "Underground", "Dump", "Graveyard", "Plain", "Debris"]
        return random.choice(first) + " " + random.choice(second)

    name = fields.Char(default=_generate_name)

    energy = fields.Float()
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()
    despair = fields.Float(default=50)  # %
    radiation = fields.Float(default=50)  # %
    junk = fields.Float(default=1000)  # junk és la "moneda" del joc

    buildings = fields.One2many('negocity.building', 'city')
    survivors = fields.One2many('negocity.survivor', 'city')
    players = fields.Many2many('negocity.player', compute='_get_players', string='Players with survivors')

    @api.depends('survivors')
    def _get_players(self):
        for c in self:
            players = []
            for s in c.survivors:
                if s.player:
                    players.append(s.player.id)
            print(players)
            c.players = players

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
            # print(positions)
            for i in range(0, 50):
                x = math.floor(positions[i] / 50)
                y = positions[i] % 50
                print(x, y)
                board[x][y] = 1
                new_city = self.create({
                    "energy": random.random() * 100,
                    "oil": random.random() * 100,
                    "food": random.random() * 100,
                    "water": random.random() * 100,
                    "radiation": random.random() * 100,
                    "position_x": x,
                    "position_y": y})
                new_cities = new_cities | new_city
                # Els edificis de la ciutat
                for i in range(0, random.randint(1, 10)):  # Pot crear fins a 10 edificis en ruines
                    tipus = random.choice(self.env['negocity.building_type'].search([]).ids)
                    self.env['negocity.building'].create({
                        'type': tipus,
                        'city': new_city.id,
                        'ruined': 100
                    })

            # Les carreteres
            all_roads = False
            i = 1
            while all_roads == False:
                all_roads = True

                for c in new_cities:
                    distancias = new_cities.sorted(key=lambda r: math.sqrt(
                        (r.position_x - c.position_x) ** 2
                        + (r.position_y - c.position_y) ** 2)
                                                   )
                    # Si no exiteix previament una igual
                    if len(distancias) > i:
                        # print('i:',i)
                        if (len(self.env['negocity.road'].search(
                                [('city_1', '=', distancias[i].id), ('city_2', '=', c.id)])) == 0):
                            # print(self.env['negocity.road'].search([('city_2','=', distancias[i].id),('city_1','=', c.id)]))
                            if (len(self.env['negocity.road'].search(
                                    [('city_2', '=', distancias[i].id), ('city_1', '=', c.id)])) == 0):
                                # print('Mateixa',c.id)
                                # Si no té colisió
                                # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
                                def ccw(A, B, C):
                                    return (C.position_y - A.position_y) * (B.position_x - A.position_x) > (
                                                B.position_y - A.position_y) * (C.position_x - A.position_x)

                                # Return true if line segments AB and CD intersect
                                def intersect(A, B, C, D):
                                    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

                                colisionen = self.env['negocity.road'].search([]).filtered(
                                    lambda r: intersect(r.city_1, r.city_2, c, distancias[i]))
                                if len(colisionen) == 0:
                                    self.env['negocity.road'].create(
                                        {'city_1': c.id, 'city_2': distancias[i].id})  # la primera és ella mateixa
                                    all_roads = False
                i = i + 1
                print(all_roads, i)

    def create_npc(self):
        for c in self:
            template = random.choice(self.env['negocity.character_template'].search([]).mapped(lambda t: t.id))
            self.env['negocity.survivor'].create({'template': template, 'city': c.id})


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
    workers = fields.Many2many('negocity.survivor')
    time = fields.Float(compute='_get_time')
    date_start = fields.Datetime()
    date_end = fields.Datetime(compute='_get_time')
    progress = fields.Float(compute='_get_time')

    @api.depends('type', 'workers','date_start')
    def _get_time(self):
        for b in self:
            n_workers = len(b.workers)
            if n_workers > 0:
                mean_illness = 0
                for w in b.workers:
                    mean_illness = mean_illness + w.illnes
                mean_illness = mean_illness / n_workers
                b.time = b.type.time / math.log10(n_workers * (100 - mean_illness))
            else:
                b.time = b.type.time

            # treure data final
            if b.date_start:
                b.date_end = fields.Datetime.to_string(
                    fields.Datetime.from_string(b.date_start) + timedelta(hours=b.time))
                time_remaining = fields.Datetime.from_string(b.date_end) - fields.Datetime.from_string(fields.datetime.now())
                print(time_remaining.total_seconds()/60/60,fields.datetime.now(),'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
                time_remaining = time_remaining.total_seconds()/60/60
                b.progress = 50 #  time_remaining / b.time  ####no funciona el time remaining !!!!
            else:
                b.date_end = ''
                b.progress = 25


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


class vehicle(models.Model):
    _name = 'negocity.vehicle'
    _description = 'vehicles'
    name = fields.Char()
   # type = fields.Selection([('truck','Truck'),('car','Car'),('bus','Bus')])
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
    # distance = fields.Float(compute='_get_distance')


class character_template(models.Model):
    _name = 'negocity.character_template'
    _description = 'Templates to generate characters'

    name = fields.Char()
    image = fields.Image(max_width=200, max_height=400)


class travel(models.Model):
    _name = 'negocity.travel'
    _description = 'Travels'

    name = fields.Char()
    origin = fields.Many2one('negocity.city', ondelete='cascade')
    destiny = fields.Many2one('negocity.city', ondelete='cascade')  # filtrat
    road = fields.Many2one('negocity.road', ondelete='cascade')  # computat
    date_departure = fields.Datetime(default=lambda r: fields.datetime.now())
    date_end = fields.Datetime(compute='_get_date_end')  # sera computat en funció de la distància

    @api.depends('date_departure', 'road')
    def _get_date_end(self):
        for t in self:
            d_dep = t.date_departure
            data = fields.Datetime.from_string(d_dep)
            data = data + timedelta(hours=3)
            t.date_end = fields.Datetime.to_string(data)

    player = fields.Many2one('negocity.player')
    passengers = fields.Many2many('negocity.survivor')  # filtrats sols els que són de la ciutat origin i del player
