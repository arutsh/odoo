# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstateAccount(models.Model):
    _name = "estate.account"
    _description = "Estate account"
    _order =  "sequence, name"

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1, help="sorting by sequance")
    #property_ids = fields.One2many("estate.property", "property_type_id", string="Properties")
