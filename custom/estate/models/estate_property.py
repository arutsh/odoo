# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Agency Properties"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    #state saves status of the property
    postcode = fields.Char()
    date_availability = fields.Date(default=(fields.Datetime.add(fields.Datetime.today(), months=3)), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
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
    total_area = fields.Float(compute="_compute_total")
    active = fields.Boolean(default=True)
    state = fields.Selection([
                        ('new', 'New'),
                        ('offer_Received', 'Offer Recieved'),
                        ('offer_accepted', 'Offer Accepted'),
                        ('sold', 'Sold'),
                        ('canceled', 'Canceled'),
                        ], required=True, copy=False, default='new')

    property_type_id = fields.Many2one("estate.property.type", string ="Property type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string = "Tags", index=True, copy=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Expected price has to be striclty positive.')
    ]

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'A property selling price must be positive.')
    ]

    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            # TODO: check if there is offer, otherwise leave empty
            if(record.offer_ids):
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = None

    @api.onchange("garden")
    def _onchange_garden(self):
        if(self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=2):
                diff = record.expected_price * 0.1
                if float_compare(diff, record.expected_price-record.selling_price, precision_digits=2)<0:
                    raise ValidationError("selling price can not be lower than 90% of the expected price")

    def action_sold(self):
        for record in self:
            if(record.state == 'offer_accepted'):
                record.state = 'sold'
            elif(record.state == 'canceled'):
                raise UserError('can not sold property which is already cancelled.')
            elif(record.state == 'offer_Received'):
                raise UserError('please accept offer first.')
            elif(record.state == 'new'):
                raise UserError('there is not offers yet')
        return True

    def action_cancel(self):
        for record in self:
            if (record.state == 'sold'):
                raise UserError('You can not cancel property if it is sold')
            else:
                record.state = 'canceled'

        return True

    def unlink(self):
        # Do some business logic, modify vals...
        ...
        # Then call super to execute the parent method
        for record in self:
            if (record.state == 'new'):
                raise UserError('You can not delete property at new state')
                return True

        return super().unlink()


class EstatePropertyType(models.Model):
    _inherit = "estate.property.type"
    property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")


class ResUsers(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many("estate.property", "salesperson_id", string="Properties")
