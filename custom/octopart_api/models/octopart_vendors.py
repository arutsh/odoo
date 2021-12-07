# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from custom.octopart_api.models.octopart_client import OctoPartClient, demo_match_mpns, demo_search_mpn


class OctoPartVendors(models.Model):
    _name = "octopart.parts.vendors"
    _description = "Retrieves Vendors from octopart "
    _order = "id desc"

    vendor_id = fields.Char(string="PartsBox ID", required=True)
    name = fields.Char(required=True)


    def create(self, val):
        if self.search([('vendor_id', '=' , val['vendor_id'])]):
            return self.search([('vendor_id', '=' , val['vendor_id'])])
        return super().create(val)


    def unlink(self):
        # Do some business logic, modify vals...
        ...
        # Then call super to execute the parent method
        #for record in self:
            #if (record.state == 'new'):
                #raise UserError('You can not delete property at new state')
        #    return True


        return super().unlink()
