import pytz
from odoo import models, fields, api, _


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='product')
    product_qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment ID")


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Appointment ID', required=True, copy=False, index=True,
                       readonly=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient', required=True)
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Register Note")
    doctor_note = fields.Text(string="Note", track_visibility='onchange')
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')
    pharmacy_note = fields.Text(string="note", track_visibility='always')
    # appointment_lines = fields.One2many("hospital.appointment.lines", 'appointment_id', string="Appointment")
    appointment_date = fields.Date(string='Date', required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Many2one('sale.order', string="Order")
    amount = fields.Float(string="Total Amount")
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('refuse', 'Refuse'),
    ], string='Status', readonly=True,
        default='draft')

    # Delete appointment_lines
    def delete_lines(self):
        for rec in self:
            print('rec', rec)
            rec.appointment_lines = [(5, 0, 0)]

    # This api is for sequence
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment.sequence') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    # This is for default field value
    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        res['notes'] = 'Enter patient condition'
        return res

    # this is for confirm button
    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': "Appointment Confirmed... Thankyou",
                    'type': 'rainbow_main',
                }
            }

    def action_refuse(self):
        for rec in self:
            rec.state = 'refuse'
    # this is for notify
    def action_notify(self):
        for rec in self:
            rec.doctor_id.user_id.notify_success(message='New appointment')

    # this is for dependent field one field for partner and other field shows its orders
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.model
    def get_default_values(self, fields):
        rec = super(HospitalAppointment, self).get_default_values(fields)
        rec['patient_id'] = 1
        return rec
