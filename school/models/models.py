# -*- coding: utf-8 -*-
import random

from odoo import models, fields, api


class school(models.Model):
     _name = 'school.school'
     _description = 'school.school'

     name = fields.Char()
     students = fields.One2many('school.student','school_id')
     token = fields.Char(compute='_get_token')

     def _get_token(self):
         print(self)
         for s in self:
             print(self)
             s.token = str(random.randint(0,10000))
             print('********************************',s.token)

class student(models.Model):
     _name = 'school.student'
     _description = 'Students'

     name = fields.Char()
     school_id = fields.Many2one('school.school',string="School")
     school_name = fields.Char(string='School Name', related='school_id.name')
     classroom = fields.Many2many('school.classroom')
     topics = fields.Many2many('school.topic')
     passed = fields.Many2many(comodel_name='school.topic', # El model en el que es relaciona
                            relation='students_passed', # (opcional) el nom del la taula en mig
                            column1='student_id', # (opcional) el nom en la taula en mig de la columna d'aquest model
                            column2='topic_id')  # (opcional) el nom de la columna de l'altre model.
     smart = fields.Float(default= lambda r: random.randint(90,150))
     nota = fields.Float(compute='_get_nota')
     registration_date=fields.Datetime()

     @api.depends('smart')
     def _get_nota(self):
         for s in self:
             s.nota = s.smart/15

     def _get_drugs(self):
         all_drugs = self.env['school.drug'].search([]).ids

         random.shuffle(all_drugs)
         drugs = []
         for i in range(0,random.randint(0,len(all_drugs))):
             drugs.append(all_drugs[i])
         return drugs

     drugs = fields.Many2many('school.drug',default=_get_drugs)



class drug(models.Model):
    _name = 'school.drug'
    _description = 'Students drugs'

    name = fields.Char()
    students = fields.Many2many('school.student')


class topic(models.Model):
     _name = 'school.topic'
     _description = 'topic'

     name = fields.Char()
     students = fields.Many2many('school.student')
     student_passed = fields.Many2many(comodel_name='school.student', # El model en el que es relaciona
                            relation='students_passed', # (opcional) el nom del la taula en mig
                            column2='student_id',
                            column1='topic_id')



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
