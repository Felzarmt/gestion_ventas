from odoo import fields, models, api  # type:ignore


class GestionVentasLinea(models.Model):
    _name = 'gestion.ventas.linea'
    _description = 'Línea de productos de una venta'

    product_id = fields.Many2one(
        'product.product', string="Producto", required=True)
    price_unit = fields.Float(string="Precio unitario")
    quantity = fields.Integer(string="Cantidad", default=1)
    subtotal = fields.Float(
        string="Subtotal", compute="_compute_subtotal", store=True)

    venta_id = fields.Many2one('gestion.ventas.ventas', string="Venta")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.lst_price

    @api.depends('price_unit', 'quantity')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.price_unit * line.quantity
