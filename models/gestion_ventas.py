from odoo import models, fields, api  # type:ignore


class GestionVentas (models.Model):

    _name = "gestion.ventas.ventas"
    _description = "Gestion de ventas para clientes"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Nombre de la venta")
    full_price = fields.Float(
        string="TOTAL", readonly=True, compute="_compute_precio_total", store=True)
    sell_date = fields.Date(string="Fecha de venta")
    state = fields.Selection([
        ("borrador", "Borrador"),
        ("confirmado", "Confirmado"),
        ("facturado", "Facturado")
    ])

    # Relaciones
    linea_ids = fields.One2many(
        "gestion.ventas.linea", "venta_id", string="Productos")
    seller = fields.Many2one("hr.employee", string="Vendedor ")
    costumer = fields.Many2one("res.partner", string="Cliente")
    invoice_id = fields.Many2one("account.move", string="Factura")

    @api.depends('linea_ids.subtotal')
    def _compute_precio_total(self):
        for record in self:
            record.full_price = sum(line.subtotal for line in record.linea_ids)

    def generar_factura(self):
        for record in self:
            if not record.costumer:
                raise ValueError("Debe seleccionar un cliente.")
            if not record.linea_ids:
                raise ValueError(
                    "Debe agregar al menos una línea de producto.")

            # Crear las líneas de factura
            lineas = []
            for linea in record.linea_ids:
                linea_factura = (0, 0, {
                    'product_id': linea.product_id.id,
                    'quantity': linea.quantity,
                    'price_unit': linea.price_unit,
                    'name': linea.product_id.name,
                    'tax_ids': [(6, 0, linea.product_id.taxes_id.ids)],
                })
                lineas.append(linea_factura)

            # Crear la factura
            factura = self.env['account.move'].create({
                'partner_id': record.costumer.id,
                'invoice_date': record.sell_date or fields.Date.today(),
                'move_type': 'out_invoice',
                'invoice_line_ids': lineas,
            })

            # Guardar la factura en el campo Many2one
            record.invoice_id = factura.id

            # Mostrar la factura generada al usuario
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': factura.id,
                'view_mode': 'form',
                'target': 'current',
            }
