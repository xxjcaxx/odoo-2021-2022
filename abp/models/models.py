# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rubrica(models.Model):
    _name = 'abp.rubrica'
    _description = 'abp.rubrica'

    name = fields.Char()
    modulo = fields.Char()
    curso = fields.Char()

class indicador(models.Model):
    _name = 'abp.indicador'
    _description = 'abp.indicador'

    name = fields.Char()
    descripcion = fields.Text()
    puntos = fields.Float()
    rubricas = fields.Many2many('abp.rubrica')
    niveles = fields.Many2many('abp.nivel')

class nivel(models.Model):
    _name = 'abp.nivel'
    _description = 'abp.nivel'

    name = fields.Char()
    descripcion = fields.Text()
    ponderacion = fields.Float()
    indicadores = fields.Many2many('abp.indicador')

class puntuacion(models.Model):
    _name = 'abp.puntuacion'
    _description = 'abp.puntuacion'

    name = fields.Char()
    indicador = fields.Many2one('abp.indicador')
    nivel = fields.Many2one('abp.nivel')
    rubrica = fields.Many2one('abp.rubrica')
    alumno = fields.Many2one('res.partner')
    logrado = fields.Boolean()
