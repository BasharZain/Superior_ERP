from odoo import models, fields, api, _

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor Record'

    name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string="Gender")
    specialist = fields.Char(string="Specialist")
    user_id = fields.Many2one('res.users', string='Related User')