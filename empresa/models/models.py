# -*- coding: utf-8 -*-

from odoo import models, fields, api, modules


class furgoneta(models.Model):
    _name = 'empresa.furgoneta'
    _description = 'empresa.furgoneta'

    matricula = fields.Char()
    capacitat = fields.Integer()
    foto = fields.Image(max_width=100, max_height=100)
    viatges = fields.One2many(string='Viatges',comodel_name='empresa.viatge',inverse_name='furgo')
    paquets = fields.Many2many('viatges.paquet',related='viatges.paquets')

    _sql_constraints = [ ('matricula_uniq','unique(matricula)','La matrícula de la furgoneta no se puede repetir') ]

class viatge(models.Model):
    _name = 'empresa.viatge'
    _description = 'empresa.viatge'

    m3 = fields.Many2one('empresa.paquet',compute='_get_m3')
    iden = fields.Integer()
    paquets = fields.One2many(string='Paquets',comodel_name='empresa.paquet',inverse_name='vi')
    conductor = fields.Many2one('res.partner')
    furgo = fields.Many2one('empresa.furgoneta', ondelete='set null')

    def _get_m3(self):
        for m in self:
            for i in m:
                m.m3 += m.paquets[i].volum
            else:
                m.m3 = 0

    @api.constrains('paquets')
    def _maxim_paquets(self):
        for s in self:
            for i in s:
            if s.furgo[i].capacitat > m3:
                print(s.furgo[i].capacitat)
            else:    
                raise ValidationError('El número de paquets excedis els de la furgoneta.')

class paquet(models.Model):
    _name = 'empresa.paquet'
    _description = 'empresa.paquet'

    iden = fields.Integer()
    volum = fields.Integer()
    vi = fields.Many2one('empresa.viatge', ondelete='set null')