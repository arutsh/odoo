# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Agency Properties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=(fields.Datetime.add(fields.Datetime.today(), months=3)), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
                                    ('north', 'North'),
                                    ('south', 'South'),
                                    ('east', 'East'),
                                    ('west', 'West'),
                                    ])
    active = fields.Boolean(default=True)
    state = fields.Selection([
                        ('new', 'New'),
                        ('offer_Received', 'Offer Recieved'),
                        ('offer_accepted', 'Offer Accepted'),
                        ('sold', 'Sold'),
                        ('canceled', 'Canceled'),
                        ], required=True, copy=False, default='new')

    property_type_id = fields.Many2one("estate.property.type", string ="Property type")
