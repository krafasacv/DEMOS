from odoo import models, fields, api


class ComisionResPartner(models.Model):
    _inherit = 'res.partner'

    x_es_comisionista = fields.Boolean('Es comisionista')
    x_comision = fields.Float('% de comisión')