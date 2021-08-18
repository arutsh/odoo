# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstateProperty(models.Model):
    _inherit = "estate.property"


    def action_sold(self):
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        print("*** INHERET ***")
        print("*** INHERET ***")
        print("*** INHERET ***")
        for record in self:
            print(self.buyer_id.id)
            partner_id = self.buyer_id.id
            price = self.selling_price *1.06
        print(journal.id)
        print("*** INHERET ***")
        print("*** INHERET ***")


        self.env['account.move'].create(
                    {
                        "partner_id":partner_id,
                        "move_type": 'out_invoice',
                        "journal_id":journal.id,
                        "invoice_line_ids":[
                                    (
                                        0,
                                        0,
                                        {
                                            "name":"house test desc + 6%",
                                            "quantity": 1,
                                            "price_unit": price,
                                        },
                                    ),
                                    (
                                        0,
                                        0,
                                        {
                                            "name":"administrative fees",
                                            "quantity": 1,
                                            "price_unit": 100,
                                        },
                                    ),

                                ],
                    }
                )

        return super().action_sold()
