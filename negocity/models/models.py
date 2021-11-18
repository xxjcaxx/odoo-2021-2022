# -*- coding: utf-8 -*-


from odoo import models, fields, api
import random
import math
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
## from odoo.exceptions import Warning   (Es considera obsolet en favor de UserError)
from odoo.exceptions import UserError


class event(models.Model):
    _name = 'negocity.event'
    _description = 'Events'

    name = fields.Char()
    player = fields.Many2many('negocity.player')
    event = fields.Reference([('negocity.building','Building'),('negocity.travel','Travel'),('negocity.collision','Collision'),('negocity.player','Player'),('negocity.survivor','Survivor')])
    description = fields.Text()

    @api.model
    def clean_messages(self):
        yesterday = fields.Datetime.to_string(datetime.now()-timedelta(hours=24))
        old_messages = self.search([('creation_date','<',yesterday)])
        old_messages.unlink()



    ### TODO

    ### 
    ### Opció de donar gasolina i junk a la ciutat
    ### Veure en una cituat els viatges que estan vinguent
    ### Les batalles es faran creuant dos viatges. Quan un player envia un viatge pot ser per anar a furtar a una ciutat o per a defendrer-la.
    ###     Un player o molts poden enviar molts viatges, com que van per la carretera, els que vinguen en direcció contraria lluitaran.
    ####    Les restes de la lluita (chatarra i gasolina) es queden en la carretera fins a que passe algú
    ### Producció dels edificis
    ### Salud i progressió dels supervivents
    ### Salud dels vehicles


    ### Wizards:  Create building , cReate travel, generate full game