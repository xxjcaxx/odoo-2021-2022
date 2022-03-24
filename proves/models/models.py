# -*- coding: utf-8 -*-

from odoo import models, fields, api


class proves(models.Model):
    _name = 'proves.proves'
    _description = 'proves.proves'

    name = fields.Char()

    def create_pos_order(self):
        self.env['pos.order'].create_from_ui([{'id': '00001-004-00060',
                                               'data': {'name': 'Orden 00001-004-00060', 'amount_paid': 0,
                                                        'amount_total': 5.32, 'amount_tax': 0.92, 'amount_return': 0,
                                                        'lines': [[0, 0,
                                                                   {'qty': 2, 'price_unit': 2.2, 'price_subtotal': 4.4,
                                                                    'price_subtotal_incl': 5.32, 'discount': 0,
                                                                    'product_id': 69, #'tax_ids': [[6, False, [187]]],
                                                                    'id': 58, 'pack_lot_ids': [], 'description': '',
                                                                    'full_product_name': 'Agua', 'price_extra': 0,
                                                                    'mp_skip': False, 'note': ''}]],
                                                        'statement_ids': [], 'pos_session_id': 1, 'pricelist_id': 1,
                                                        'partner_id': False, 'user_id': 2, 'uid': '00001-004-0004',
                                                        'sequence_number': 4,
                                                        'creation_date': '2021-10-22T16:23:55.522Z',
                                                        'fiscal_position_id': False, 'server_id': False,
                                                        'to_invoice': False, 'is_tipped': False, 'tip_amount': 0,
                                                        'table': 'T2', 'table_id': 2, 'floor': 'Main Floor',
                                                        'floor_id': 1, 'customer_count': 1}, 'to_invoice': False}],
                                             True)

    def create_pos_line(self):
        self.env['pos.order.line'].create({
            'order_id': 1,
            'full_product_name': 'AAAAAAAAAAA',
            'qty': 1,
            'product_id': 70,
            'price_subtotal': 40,
            'price_subtotal_incl': 45
        })
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
