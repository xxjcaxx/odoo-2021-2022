# -*- coding: utf-8 -*-

from odoo import models, fields, api


class rubrica(models.Model):
    _name = 'abp.rubrica'
    _description = 'abp.rubrica'

    name = fields.Char()
    modulo = fields.Char()
    curso = fields.Char()
    indicadores = fields.Many2many('abp.indicador')
    niveles = fields.Many2many('abp.nivel', compute='_get_niveles')

    @api.depends('indicadores')
    def _get_niveles(self):
        for r in self:
            r.niveles = r.indicadores.niveles

class indicador(models.Model):
    _name = 'abp.indicador'
    _description = 'abp.indicador'

    name = fields.Char()
    descripcion = fields.Text()
    puntos = fields.Float()
    rubricas = fields.Many2many('abp.rubrica')
    niveles = fields.One2many('abp.nivel', 'indicador')

class nivel(models.Model):
    _name = 'abp.nivel'
    _description = 'abp.nivel'

    name = fields.Char()
    descripcion = fields.Text()
    ponderacion = fields.Float()
    indicador = fields.Many2one('abp.indicador')

class puntuacion(models.Model):
    _name = 'abp.puntuacion'
    _description = 'abp.puntuacion'

    name = fields.Char()
    indicador = fields.Many2one(related='nivel.indicador')
    nivel = fields.Many2one('abp.nivel')
    rubrica = fields.Many2one('abp.rubrica_alumno')

    logrado = fields.Boolean()

class rubrica_alumno(models.Model):
    _name = 'abp.rubrica_alumno'
    _description = 'abp.rubrica_alumno'
    _inherits = {'abp.rubrica':'rubrica_id'}

    name = fields.Char()
    alumno = fields.Many2one('res.partner')
    puntuaciones = fields.One2many('abp.puntuacion', 'rubrica')
    rubrica_id = fields.Many2one('abp.rubrica')

    def rellenar_puntuaciones(self):
        for r in self:
            niveles = r.indicadores.niveles
            for n in niveles:
                self.env['abp.puntuacion'].create({
                    'name': str(r.name)+" "+str(n.indicador.name)+" "+str(n.name),
                    'nivel': n.id,
                    'rubrica': r.id,
                    'logrado': False
                })


class View(models.Model):
    _inherit = "ir.ui.view"
    type = fields.Selection(
        selection_add=[("rubrica","Rubrica")]
    )
