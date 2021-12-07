# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MrpBomProcurement(models.Model):
     _name="mrp.bom.procurement"
     _description = "Enhanced view of BOM for procurement team"

     _inherits = {
        'mrp.bom':'bom_line_ids',
        'mrp.bom':'product_id',
        }
