# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection([
                             ('accepted', 'Accepted'),
                             ('refused', 'Refused'),
                            ], copy=False)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_id = fields.Many2one("estate.property", string="Property")
    #active = fields.Boolean(default=True)
