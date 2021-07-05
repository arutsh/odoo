# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(required=True)
    #garden_orientation = fields.Selection([
    #                                ('north', 'North'),
    #                                ('south', 'South'),
    #                                ('east', 'East'),
    #                                ('west', 'West'),
    #                                ])
    #active = fields.Boolean(default=True)
