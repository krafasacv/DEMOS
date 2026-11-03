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
        for invoice in self:
            invoice.x_status_comision = 'paid'
            invoice.x_fecha_comision = date.today()
                