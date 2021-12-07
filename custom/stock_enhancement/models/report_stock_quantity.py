# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools, api


class ReportStockQuantity(models.Model):
    _inherit = 'report.stock.quantity'

    #bom_line_id = fields.Many2one('mrp.bom.line', string="BOM", readonly=True)
    cumulative_quantity = fields.Float(string='Cumulative Quantity', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self._cr, 'report_stock_quantity')
        query = """CREATE or REPLACE VIEW report_stock_quantity AS (
SELECT
    MIN(id) as id,
    product_id as product_id,
	'in' as state,
    to_char(date, 'YYYY-MM-DD') as date,
    sum(product_qty) AS product_qty,
    sum(sum(product_qty)) OVER (PARTITION BY product_id ORDER BY date) AS cumulative_quantity,
    company_id
    FROM
    (SELECT
    MIN(id) as id,
    MAIN.product_id as product_id,
    SUB.date as date,
    CASE WHEN MAIN.date = SUB.date THEN sum(MAIN.product_qty) ELSE 0 END as product_qty,
    MAIN.company_id as company_id
    FROM
    (SELECT
        MIN(sq.id) as id,
        sq.product_id,
	 	'in' as state,
        date_trunc('week', to_date(to_char(CURRENT_DATE, 'YYYY/MM/DD'), 'YYYY/MM/DD')) as date,
        SUM(sq.quantity) AS product_qty,
        sq.company_id
        FROM
        stock_quant as sq
        LEFT JOIN
        product_product ON product_product.id = sq.product_id
        LEFT JOIN
        stock_location location_id ON sq.location_id = location_id.id
        WHERE
        location_id.usage = 'internal'
        GROUP BY date, sq.product_id, sq.company_id
        UNION ALL
        SELECT
        MIN(-sm.id) as id,
        sm.product_id,
	 	'in' as state,
        CASE WHEN sm.date_deadline > CURRENT_DATE
        THEN date_trunc('week', to_date(to_char(sm.date_deadline, 'YYYY/MM/DD'), 'YYYY/MM/DD'))
        ELSE date_trunc('week', to_date(to_char(CURRENT_DATE, 'YYYY/MM/DD'), 'YYYY/MM/DD')) END
        AS date,
        SUM(sm.product_qty) AS product_qty,
        sm.company_id
        FROM
           stock_move as sm
        LEFT JOIN
           product_product ON product_product.id = sm.product_id
        LEFT JOIN
        stock_location dest_location ON sm.location_dest_id = dest_location.id
        LEFT JOIN
        stock_location source_location ON sm.location_id = source_location.id
        WHERE
        sm.state IN ('confirmed','partially_available','assigned','waiting') and
        source_location.usage != 'internal' and dest_location.usage = 'internal'
        GROUP BY sm.date_deadline,sm.product_id, sm.company_id
        UNION ALL
        SELECT
            MIN(-sm.id) as id,
            sm.product_id,
	 		'in' as state,
            CASE WHEN sm.date_deadline > CURRENT_DATE
                THEN date_trunc('week', to_date(to_char(sm.date_deadline, 'YYYY/MM/DD'), 'YYYY/MM/DD'))
                ELSE date_trunc('week', to_date(to_char(CURRENT_DATE, 'YYYY/MM/DD'), 'YYYY/MM/DD')) END
            AS date,
            SUM(-(sm.product_qty)) AS product_qty,
            sm.company_id
        FROM
           stock_move as sm
        LEFT JOIN
           product_product ON product_product.id = sm.product_id
        LEFT JOIN
           stock_location source_location ON sm.location_id = source_location.id
        LEFT JOIN
           stock_location dest_location ON sm.location_dest_id = dest_location.id
        WHERE
            sm.state IN ('confirmed','partially_available','assigned','waiting') and
        source_location.usage = 'internal' and dest_location.usage != 'internal'
        GROUP BY sm.date_deadline,sm.product_id, sm.company_id)
     as MAIN
 LEFT JOIN
 (SELECT DISTINCT date
  FROM
  (
         SELECT date_trunc('week', CURRENT_DATE) AS DATE
         UNION ALL
         SELECT date_trunc('week', to_date(to_char(sm.date_deadline, 'YYYY/MM/DD'), 'YYYY/MM/DD')) AS date
         FROM stock_move sm
         LEFT JOIN
         stock_location source_location ON sm.location_id = source_location.id
         LEFT JOIN
         stock_location dest_location ON sm.location_dest_id = dest_location.id
         WHERE
         sm.state IN ('confirmed','assigned','waiting') and sm.date_deadline > CURRENT_DATE and
         ((dest_location.usage = 'internal' AND source_location.usage != 'internal')
          or (source_location.usage = 'internal' AND dest_location.usage != 'internal'))) AS DATE_SEARCH)
         SUB ON (SUB.date IS NOT NULL)
GROUP BY MAIN.product_id,SUB.date, MAIN.date, MAIN.company_id
) AS FINAL
GROUP BY product_id,date,company_id
)"""
        self.env.cr.execute(query)
