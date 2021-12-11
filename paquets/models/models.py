# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class furgoneta(models.Model):
     _name = 'paquets.furgoneta'
     _description = 'furgoneta'

     name = fields.Char(string="matricula")
     capacitat = fields.Float()
     viatges = fields.One2many('paquets.viatge','furgoneta')
     foto = fields.Image(max_width = 200, max_heigth=200)
     paquets = fields.Many2many('paquets.paquet',compute='_get_paquets')
     paquets2 = fields.One2many('paquets.paquet',related='viatges.paquets')

     @api.depends('viatges')
     def _get_paquets(self):
         for f in self:
            f.paquets = f.viatges.paquets

     _sql_constraints = [('matricula_uniq', 'unique(name)', 'No es pot repetir matrícula')]

class viatge(models.Model):
     _name = 'paquets.viatge'
     _description = 'viatge'

     name = fields.Char(string="identificador")
     conductor = fields.Many2one('res.partner')
     espai_aprofitat = fields.Float(compute='_get_aprofitat')
     furgoneta = fields.Many2one('paquets.furgoneta')
     capacitat = fields.Float(related='furgoneta.capacitat')
     paquets = fields.One2many('paquets.paquet','viatge')

     @api.depends('furgoneta','paquets')
     def _get_aprofitat(self):
         for v in self:
             v.espai_aprofitat = sum(v.paquets.mapped('volum'))

     _sql_constraints = [('id_viatge_uniq', 'unique(name)', 'No es pot repetir identificador')]


   #  @api.constrains('furgoneta','paquets')
   #  def _check_capacitat(self):
   #      for v in self:
   #          if v.espai_aprofitat > v.furgoneta.capacitat:
   #              raise ValidationError("No caben tots els paquets")


class paquet(models.Model):
     _name = 'paquets.paquet'
     _description = 'paquet'

     name = fields.Char(string="identificador")
     volum = fields.Float()
     viatge = fields.Many2one('paquets.viatge')

     _sql_constraints = [('id_paquet_uniq', 'unique(name)', 'No es pot repetir identificador')]

     @api.constrains('volum','viatge')
     def _check_capacitat(self):
         for p in self:
             if p.viatge.espai_aprofitat > p.viatge.furgoneta.capacitat:
                  raise ValidationError("No cap aquest paquet"+p.name)