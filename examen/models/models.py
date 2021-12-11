# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import logging
import re
from odoo.exceptions import ValidationError

class furgoneta(models.Model):
    _name = 'examen.furgoneta'
    _description = 'examen.furgoneta'

    name = fields.Char(string="La matricula")
    
    @api.constrains('name')
    def _check_name(self):
        regex = re.compile('[0-9]{3}[a-z]\Z', re.I)
        for s in self:
            if regex.match(s.name):
                print('El numero acreditacio es valid')
            else:
                raise ValidationError('El numero de acreditacio no es valid. (3 numeros i una lletra)')

    _sql_constraints = [('name_uniq','unique(name)','La matricula no es pot repetir')]

    capacitat = fields.Integer(string="Capacitat")
    foto = fields.Image() 
    llistat_paquets = fields.Many2many('examen.paquet','identificador_paquet', help='Llistat paquets de ixa furgoneta')

    @api.depends('name')
    def compute_display_name(self):
        # This will be called every time the field is viewed
        pass

class viatge(models.Model):
    _name = 'examen.viatge'
    _description = 'examen.viatge'

    conductor = fields.Many2many('res.partner')
    identificador = fields.Integer(string="Identificador viatge")
    furgoneta = fields.Many2one('examen.furgoneta','name', help='Una furgoneta pot tindre varios viatges')
    llista_paquets = fields.One2many('examen.paquet','identificador_paquet', help='Una llista de paquets')
    metresAprofitats = fields.Integer(string="Capacitat")

    @api.depends('identificador')
    def compute_display_name(self):
        # This will be called every time the field is viewed
        pass


class paquet(models.Model):
    _name = 'examen.paquet'
    _description = 'examen.paquet'

    identificador_paquet = fields.Integer(string="Identificador paquet")
    _sql_constraints = [('name_uniq','unique(identificador_paquet)','El numero de paquet no es pot repetir')]

    volum_paquet = fields.Integer(string="Volum paquet en m3")
