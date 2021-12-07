
from odoo import _, api, fields, models, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    shortage_date = fields.Date(string="Shortage date", readonly = True, compute='_computeVar')
    shortage_qty = fields.Float(string="Shortage qty", readonly = True, compute='_computeVar')

    @api.depends('product_variant_id')
    def _computeVar(self):
        result = self.env.cr.dictfetchall()
        print("***************")
        print(result)
        print("***************")
        for rec in self:
            for item in result:
                if(item.product_id == rec.product_tmpl_id):
                    rec.shortage_date = item.shortage_date
                    rec.shortage_qty = item.shortage_qty



    def init(self):
        query = '''Select
        product_id,
date as shortage_date,
quantity as shortage_qty
From
(SELECT
    MIN(id) as id,
    product_id as product_id,
	'in' as state,
    to_char(date, 'YYYY-MM-DD') as date,
    sum(product_qty) AS quantity,
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
GROUP BY product_id,date,company_id ) as D
Where quantity < 0
ORDER by date
 '''

        self.env.cr.execute(query)
