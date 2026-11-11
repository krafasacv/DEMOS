from odoo import models, fields, api
from datetime import date


class ComisionAccountMove(models.Model):
    _inherit = 'account.move'

    x_comisionista = fields.Many2one('res.partner', string='Comisionista', readonly=True)
    x_comision = fields.Float('Comisión', readonly=True)
    x_status_comision = fields.Selection([
        ('no', 'Sin comisión'),
        ('comision', 'Comisión'),
        ('to_pay', 'Para pagar'),
        ('paid', 'Pagada'),], string='Status Comisión', readonly=True,
        compute = '_compute_status_comision',
        store=True,
        help=" * Sin comisión: No hay que pagar comisión.\n"
             " * Comisión: Tiene comisión pero NO se debe pagar aún.\n"
             " * Para pagar: La comisión puede pagarse la venta ya fue cobrada.\n"
             " * Pagada: La comisión ya fue pagada.")
    
    x_fecha_comision = fields.Date('Fecha de pago')
    x_prueba = fields.Char('para pruebas')


    @api.depends('status_in_payment')
    def _compute_status_comision(self):
        for record in self:
            if record.x_comisionista:
                if record.x_status_comision != 'paid':
                    if record.status_in_payment != 'paid':
                        record.x_status_comision = 'comision'
                    elif record.status_in_payment == 'paid':
                        record.x_status_comision = 'to_pay'
            else:
                record.x_status_comision = 'no'
    
    def pagar_comision(self):
        ref = 'Comisiones de las ventas: '
        invoice_line_vals = []
        producto = self.env['product.product'].search([('product_tmpl_id', '=', 367)])

        values = {
            'ref': '',
            'move_type': 'in_invoice',
            'narration': ref,
            'currency_id': self.currency_id.id,
            'invoice_date': date.today(),
            #'campaign_id': self.campaign_id.id,
            #'medium_id': self.medium_id.id,
            #'source_id': self.source_id.id,
            #'team_id': self.team_id.id,
            'partner_id': '',
            #'partner_shipping_id': self.partner_shipping_id.id,
            #'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id._get_fiscal_position(self.partner_invoice_id)).id,
            #'invoice_origin': self.name,
            #'invoice_payment_term_id': self.payment_term_id.id,
            #'preferred_payment_method_line_id': self.preferred_payment_method_line_id.id,
            #'invoice_user_id': self.user_id.id,
            #'payment_reference': self.reference,
            #'transaction_ids': [Command.set(txs_to_be_linked.ids)],
            'company_id': self.company_id.id,
            'invoice_line_ids': invoice_line_vals,
            'user_id': self.user_id.id,
            }
        for invoice in self:
            ref += ' '  + invoice.name 
            invoice.x_status_comision = 'paid'
            invoice.x_fecha_comision = date.today()
            res = {
            'display_type': 'product',
            'name': 'Comision de: ' + invoice.name,
            'product_id': producto.id,
            'product_uom_id': producto.uom_id.id,
            'quantity': 1,
            #'discount': self.discount,
            'price_unit': invoice.x_comision,
            'tax_ids': [(6, 0, producto.supplier_taxes_id.ids)],
            #'purchase_line_id': self.id,
            #'is_downpayment': self.is_downpayment,
        }

            invoice_line_vals.append((0, 0, res))

            
            
        invoice.x_prueba = values
        values.update({'partner_id': invoice.x_comisionista.id,'invoice_line_ids': invoice_line_vals,'ref': ref})
        AccountMove = self.env['account.move'].with_context(default_move_type='in_invoice')
        AccountMove.with_company(self.company_id.id).create(values)