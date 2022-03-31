# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random


class teamTemplate(models.Model):
    _name = 'pcfutbol.team'

    _description = 'Team teamplates'

    name = fields.Char()
    shield = fields.Image(max_width = 200)   

class team(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Teams'

    team_template = fields.Many2one('pcfutbol.team')
    #players = fields.One2many('pcfutbol.player','team')
    money = fields.Float()
    leagues = fields.Many2many('pcfutbol.league')
    shield = fields.Image(max_width = 200)

class player(models.Model):
    _name = 'pcfutbol.player'
    _description = 'Players'

    name = fields.Char()
    team = fields.Many2one('pcfutbol.team',ondelete='set null')
    points = fields.Integer()
    position = fields.Selection([('1','Portero'),('2','Defensa'),('3','Centrocampista'),('4','Delantero')])
    price = fields.Float()
    state = fields.Selection([('ok','Ok'),('doubtful','Dudoso'),('injured','Lesionado'),('suspended','Suspendido')])
    image = fields.Image(max_width = 200)
    team_shield = fields.Image(related = 'team.shield', max_width = 100)


class league(models.Model):
    _name = 'pcfutbol.league'
    _description = 'League'

    name = fields.Char()
    teams = fields.Many2many('res.partner')
    matches = fields.One2many('pcfutbol.match','league')

    def view_journeys(self):  # La manera de fer una especie de group by en un tree intern
        return {
            'name': 'Display Journeys',
            'view_mode': 'tree',
            'res_model': 'pcfutbol.match',
            'domain': [('id', 'in', self.matches.ids)],
            'context': {'group_by': ['journey']},
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    def create_calendar(self):
        for league in self:
            # Primer esborrar tot
            league.matches.unlink()
            teams_ids = self.teams.ids
            print(teams_ids)
            random.shuffle(teams_ids)
            for i in range(1, len(teams_ids)):
                print(teams_ids,i)
                day =  i
                day2 = i + len(teams_ids) - 1

                for j in range(0, int(len(teams_ids) / 2)):  # Primera volta
                    if i % 2 == 0:  # alternar en casa o visitant
                        team_a = teams_ids[j]
                        team_b = teams_ids[len(teams_ids) - 1 - j]
                    else:
                        team_b = teams_ids[j]
                        team_a = teams_ids[len(teams_ids) - 1 - j]
                    self.env['pcfutbol.match'].create({
                        'name': str(day)+" "+str(team_a)+" "+str(team_b),
                        'journey': day,
                        'local': team_a,
                        'visitor': team_b,
                        'league': league.id
                    })

                for j in range(0, int(len(teams_ids) / 2)):  # Segona volta
                    if i % 2 == 0:  # alternar en casa o visitant
                        team_a = teams_ids[j]
                        team_b = teams_ids[len(teams_ids) - 1 - j]
                    else:
                        team_b = teams_ids[j]
                        team_a = teams_ids[len(teams_ids) - 1 - j]
                    self.env['pcfutbol.match'].create({
                        'name': str(day) + " " + str(team_a) + " " + str(team_b),
                        'journey': day2,
                        'local': team_a,
                        'visitor': team_b,
                        'league': league.id
                    })

                aux = []
                aux.append(teams_ids[0])
                aux.append(teams_ids[len(teams_ids) - 1])
                aux.extend(teams_ids[1:len(teams_ids) - 1])
                teams_ids = aux



class match(models.Model):
    _name = 'pcfutbol.match'
    _description = 'Match'

    name = fields.Char()
    journey = fields.Integer(required=True)
    local = fields.Many2one('res.partner', ondelete='cascade', required=True)
    visitor = fields.Many2one('res.partner', ondelete='cascade',required=True)
    league = fields.Many2one('pcfutbol.league', ondelete='cascade',required=True)
    winner = fields.Many2one('res.partner',ondelete='set null')
    goals = fields.Char()

    @api.constrains('local','visitor','league')
    def _check_teams(self):
        for match in self:
            if match.local not in match.league.teams:
                raise ValidationError('Local team is not a from this league')
            if match.visitor not in match.league.teams:
                raise ValidationError('Visitor team is not a from this league')
            if match.local == match.visitor:
                raise ValidationError('Same Teams')

    @api.onchange('league')
    def _onchangue_league(self):
        if self.league != False:
            return {
                'domain': {
                    'local': [('id','in',self.league.teams.ids)],
                    'visitor': [('id', 'in', self.league.teams.ids)]
                }
            }


