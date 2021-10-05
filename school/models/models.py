# -*- coding: utf-8 -*-

from odoo import models, fields, api


class school(models.Model):
     _name = 'school.school'
     _description = 'school.school'

     name = fields.Char()
     students = fields.One2many('school.student','school_id')

class student(models.Model):
     _name = 'school.student'
     _description = 'Students'

     name = fields.Char()
     school_id = fields.Many2one('school.school',string="School")
     classroom = fields.Many2many('school.classroom')

class classroom(models.Model):
     _name = 'school.classroom'
     _description = 'Classrooms'

     name = fields.Char()
     students = fields.Many2many('school.student')
#     value = fields.Integer(s)
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
