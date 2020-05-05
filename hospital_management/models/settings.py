from ast import literal_eval

from odoo import api, fields, models

class HospitalSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    note = fields.Char(string='Note')
    module_crm = fields.Boolean(string='CRM')
    product_ids = fields.Many2many('product.product', string="Medicines")

#api for the setting area where you enter record and then get record
    def set_values(self):
        res = super(HospitalSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('hospital_management.note', self.note)
        self.env['ir.config_parameter'].set_param('hospital_management.product_ids', self.product_ids.ids)
        return res

    @api.model
    def get_values(self):
        res = super(HospitalSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        notes = ICPSudo.get_param('hospital_management.note')
        product_ids = self.env['ir.config_parameter'].sudo().get_param('hospital_management.product_ids')
        res.update(
            note=notes,
            product_ids=[(6, 0, literal_eval(product_ids))],
        )
        return res