# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="price")
    status = fields.Selection([
                             ('accepted', 'Accepted'),
                             ('refused', 'Refused'),
                            ], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_id = fields.Many2one("estate.property", string="Property")
    #active = fields.Boolean(default=True)
    validity = fields.Integer(string="Valid for", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'An offer price must be strictly positive.')
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if(record.create_date):
                record.date_deadline = record.create_date + timedelta(days = record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days = record.validity)

    def _inverse_deadline(self):
        for record in self:
            if(record.create_date ):
                record.validity = (record.date_deadline - record.create_date.date()).days


    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            if(record.property_id.buyer_id == record.partner_id):
                record.property_id.buyer_id = None
                record.property_id.selling_price = 0

        return True


    @api.model
    def create(self, vals):
        for record in self.env['estate.property'].browse(vals['property_id']):
            if(vals['price'] < record.best_price):
                raise UserError('Your offer is lower than best price')
                return True

            record.state = 'offer_Received'
        return super().create(vals)
