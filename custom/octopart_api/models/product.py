# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models
from odoo.tools.float_utils import float_round, float_is_zero


class ProductTemplate(models.Model):
    _inherit = "product.template"

    linked_part_ids = fields.One2many('octopart.parts', 'linked_part_id')
    manufacturers_ids = fields.Many2many('octopart.parts.manufacturers', 'manufacturer_id')

    currency_id = fields.Many2one('res.currency', 'Currency', required=True)
    min_price = fields.Monetary(currency_field='currency_id', string="Min Price", compute="_compute_min_price")
    max_price = fields.Monetary(currency_field='currency_id', string="Max Price", compute="_compute_max_price")
    avg_price = fields.Monetary(currency_field='currency_id', compute="_compute_avg_price", string = "Avg Price")



    @api.depends("linked_part_ids.min_price")
    def _compute_min_price(self):
        for record in self:
            if (record.linked_part_ids):
                record.min_price = min(record.linked_part_ids.mapped('min_price'))
            else:
                record.min_price = None

    @api.depends("linked_part_ids.max_price")
    def _compute_max_price(self):
        for record in self:
            if (record.linked_part_ids):
                record.max_price = max(record.linked_part_ids.mapped('max_price'))
            else:
                record.max_price = None


    @api.depends("linked_part_ids.avg_price")
    def _compute_avg_price(self):
        for record in self:
            if(record.linked_part_ids):
                s =  sum(record.linked_part_ids.mapped('avg_price'))
                l =  len(record.linked_part_ids.mapped('avg_price'))
                record.avg_price = s/l
            else:
                record.avg_price = None

#    @api.onchange("linked_part_ids")
    #def _update_manufacturers_list(self):


class ProductProduct(models.Model):
    _inherit = "product.product"
