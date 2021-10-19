# -*- coding: utf-8 -*-

from odoo import models, fields, api


class proves(models.Model):
     _name = 'proves.proves'
     _description = 'proves.proves'

     name = fields.Char()


     def create_pos_line(self):
          self.env['pos.order.line'].create({
               'order_id': 1,
               'full_product_name': 'AAAAAAAAAAA',
               'qty': 1,
               'product_id': 70,
               'price_subtotal':40,
               'price_subtotal_incl':45
          })
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
