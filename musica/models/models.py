# -*- coding: utf-8 -*-

from odoo import models, fields, api


class musica(models.Model):
     _name = 'musica.song'
     _description = 'musica.song'

     name = fields.Char()
     clients = fields.Many2many('res.partner')
     popularity = fields.Integer()

     @api.model
     def update_popularity(self):
         for s in self.search([]):
             s.popularity -= 1
             print('popularity',s.popularity)



class client(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    songs = fields.Many2many('musica.song')


class song_wizard(models.TransientModel):
     _name = 'musica.song_wizard'

     def _get_client(self):
         return self.env['res.partner'].browse(self._context.get('active_id'))

     song = fields.Many2one('musica.song')
     client = fields.Many2one('res.partner', default = _get_client)

     def add(self):
          self.song.write({'clients': [(4,self.client.id,0)]})
          self.song.popularity += 100
     

