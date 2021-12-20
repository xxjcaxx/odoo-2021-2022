# -*- coding: utf-8 -*-
from odoo import fields, models


class View(models.Model):
    _inherit = "ir.ui.view"
    type = fields.Selection(
        selection_add=[("basic_view", "Basic View")]
    )


class slider(models.Model):
    _name = 'provesowl.slider'

    name = fields.Float(default=25)