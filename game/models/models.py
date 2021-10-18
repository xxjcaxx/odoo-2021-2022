# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
     _name = 'game.player'
     _description = 'El jugador'

     name = fields.Char()

class fortress(models.Model):
    _name = 'game.fortress'
    _description = 'Fortress'

    name = fields.Char()
    player_id = fields.Many2one('game.player')

