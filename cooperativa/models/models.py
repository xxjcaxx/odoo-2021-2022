# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class camio(models.Model):
     _name = 'cooperativa.camio'
     _description = 'Camions'

     name = fields.Char(string='Identificador')
     matricula = fields.Char()
     caixons = fields.Integer(default=500)
     soci = fields.Many2one('cooperativa.soci')
     arrobes = fields.Float(compute='_get_arrobes')
     kilos = fields.Float(compute='_get_arrobes')

     @api.depends('caixons')
     def _get_arrobes(self):
          for camio in self:
               camio.arrobes = camio.caixons * 1.5
               camio.kilos = camio.arrobes * 13.5

     @api.constrains('caixons')
     def _check_caixons(self):
          for c in self:
               if c.caixons > 1000:
                    raise ValidationError("Massa caixons: %s" % c.caixons)



class soci(models.Model):
     _name = 'cooperativa.soci'
     _description = 'Socis'

     name = fields.Char()
     camions = fields.One2many('cooperativa.camio','soci')
     qt_camions = fields.Integer(string="Quantitat de Camions", compute='_get_camions')
     arrobes = fields.Float(compute='_get_camions')

     @api.depends('camions')
     def _get_camions(self):
          for soci in self:
               soci.qt_camions = len(soci.camions)
               arrobes = 0
               for c in soci.camions:
                    arrobes = arrobes + c.arrobes
               soci.arrobes = arrobes


#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
