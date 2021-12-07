# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from custom.octopart_api.models.octopart_client import OctoPartClient, demo_match_mpns, demo_search_mpn


class OctoPartParts(models.Model):
    _name = "octopart.parts"
    _description = "Retrieves date from octopart by part name"
    _order = "id desc"

    avail_ids = fields.One2many("octopart.parts.availability", "avail_id")
    part_id = fields.Char(string="PartsBox ID", required=True)
    name = fields.Char(required=True)
    date = fields.Date(default=(fields.Datetime.today()),string="Last updated", copy=False)
    manufacturer = fields.Many2one('octopart.parts.manufacturers',required=True)
    manufacturer_url = fields.Char()
    description = fields.Text()
    octopart_url = fields.Char()
    image = fields.Char()
    currency_id = fields.Many2one('res.currency', 'Currency', required=True)
    linked_part_id = fields.Many2one('product.template', 'Link to Product')
    min_price = fields.Monetary(currency_field='currency_id', compute="_compute_min_price", readonly=True)
    max_price = fields.Monetary(currency_field='currency_id', compute="_compute_max_price", readonly=True)
    avg_price = fields.Monetary(currency_field='currency_id', compute="_compute_avg_price", readonly=True)
    #_sql_constraints = [
    #    ('check_selling_price', 'CHECK(selling_price >= 0)',
    #     'A property selling price must be positive.')
    #]
    @api.depends("avail_ids.price")
    def _compute_min_price(self):
        for record in self:
            if(record.avail_ids):
                record.min_price = min(record.avail_ids.mapped('price'))
            else:
                record.min_price = None

    @api.depends("avail_ids.price")
    def _compute_max_price(self):
        for record in self:
            if(record.avail_ids):
                record.max_price = max(record.avail_ids.mapped('price'))
            else:
                record.max_price = None

    @api.depends("avail_ids.price")
    def _compute_avg_price(self):
        for record in self:
            if(record.avail_ids):
                s =  sum(record.avail_ids.mapped('price'))
                l =  len(record.avail_ids.mapped('price'))
                record.avg_price = s/l
            else:
                record.avg_price = None

    def _is_part_exist(self, part_id):
        if self.search([('part_id', '=' , part_id)]):
            raise UserError("part already exist")
            return True
        return False


    @api.onchange('name')
    def _match_parts(self):
        print("_____selecting values")
        client = OctoPartClient('https://octopart.com/api/v4/endpoint')
        client.inject_token('10d26abe-cb84-476c-b2b7-a18b60ef3312')
        mpn = self.name
        result = demo_match_mpns(client, str(mpn))
        for match in result:
            for part in match['parts']:
                if (self._is_part_exist(part['id'])):
                    self.name = ""
                else:
                    self.part_id = part['id']

                    self.manufacturer = self.env['octopart.parts.manufacturers'].create({
                    'manufacturer_id':part['manufacturer']['id'],
                    'name':part['manufacturer']['name']
                    }).id

                    #self.manufacturer = part['manufacturer']['name']
                    if part['manufacturer_url'] != None:
                        self.manufacturer_url = '<a href= "' + part['manufacturer_url']+'" target="_blank"> Manufacturer URL </a>'
                    self.description = part['short_description']
                    if part['octopart_url'] != None:
                        self.octopart_url = '<a href= "' + part['octopart_url'] +'" target="_blank">Octopart URL</a>'
                    if part['best_image']['url']  != None:
                        self.image = '<img src = "' + part['best_image']['url'] + '" width="150px">'



    def check_availability(self):
        print("_____adding values")
        client = OctoPartClient('https://octopart.com/api/v4/endpoint')
        client.inject_token('10d26abe-cb84-476c-b2b7-a18b60ef3312')
        mpn = self.name
        print(self.currency_id.name)
        curr = self.currency_id.name
        q = demo_search_mpn(client, mpn, curr)

        result = q['data']['search']['results']
        avail_ids = []
        for match in result:
            part_id = match['part']['id']
            if part_id != self.part_id:
                continue
            name = match['part']['mpn']
            for sellers in match['part']['sellers']:
                seller = self.env['octopart.parts.vendors'].create({
                'vendor_id':sellers['company']['id'],
                'name':sellers['company']['name']
                }).id
                #seller = sellers['company']['name']
                for offers in sellers['offers']:
                    stock_level = offers['inventory_level']
                    stock_avail = 'false'
                    if stock_level > 0 :
                        stock_avail='true'
                    offer_url = '<a href= "' + offers['click_url'] +'" target="_blank">website</a>'
                    sku = offers['sku']
                    moq = offers['moq']
                    for p in offers['prices']:
                        price = p['converted_price']
                        currency = p['currency']
                        batch_qty = p['quantity']
                        #create record for each seller and price groupe
                        ret = self.env['octopart.parts.availability'].create({
                            'avail_id': self.id,
                            'currency_id': self.currency_id.id,
                            'part_id':part_id,
                            'name':name,
                            'seller':seller,
                            'stock_level': stock_level,
                            'stock_avail': stock_avail,
                            'sku': sku,
                            'moq': moq,
                            'price': price,
                            'currency': currency,
                            'batch_qty': batch_qty,
                            'offer_url': offer_url
                        })


    def unlink(self):
        # Do some business logic, modify vals...
        ...
        # Then call super to execute the parent method
        #for record in self:
            #if (record.state == 'new'):
                #raise UserError('You can not delete property at new state')
        #    return True
        for record in self:
            if (record.avail_ids):
                raise UserError('You can not delete Part, if there availability parts associated with it. Please delete availability list first')
                return True
        return super().unlink()
