from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # @api.model
    # def create(self, vals_list):
    #     res = super(ResPartner, self).create(vals_list)
    #     print("yes working")
    #     return res


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    #This is override existing function
    def action_confirm(self):
        print("odoo mates")
        res = super(SaleOrderInherit, self).action_confirm()
        return res

    patient_id = fields.Many2one('hospital.patient', string='Patient Name')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection_add=[('management', 'Hospital Management')])


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    _rec_name = 'patient_name'

    name = fields.Char(string='Contact Number')
    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    patient_name = fields.Char(string='Name', required='True')
    # THis is a toggle field
    # patient_age2 = fields.Float(string='Age 2')
    patient_age = fields.Integer('Age', track_visibility='always', group_operator=False)
    # The group operator is to remove it from group bar where age gets addup
    age_group = fields.Selection([('major', 'Major'), ('minor', 'Minor')], string='Age Group', compute='set_age_group',
                                 store=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], default='male', string='Gender')
    disease = fields.Char('Disease')
    notes = fields.Text(string='Discription')
    image = fields.Binary(string='Image')
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count')
    active = fields.Boolean(string='Active', default=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    doctor_gender = fields.Selection([('male', 'Male'),
                                      ('female', 'Female')], string="Doctor Gender")
    email = fields.Char(string="Email")
    pro = fields.Many2one('res.users', string="PRO")
    patient_name_upper = fields.Char(compute='compute_upper_name', inverse='inverse_upper_name')

    # this api is for name upper or lower alphabets

    @api.depends('patient_name')
    def compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper = rec.patient_name.upper() if rec.patient_name else False

    def inverse_upper_name(self):
        for rec in self:
            rec.patient_name = rec.patient_name_upper.lower() if rec.patient_name_upper else False

    # this function is to get name with sequence
    def name_get(self):
        res = []
        for ddt in self:
            res.append((ddt.id, ("%s (%s)") % (ddt.name_seq, ddt.patient_name)))
        return res

    # Email sending template
    def action_send_card(self):
        # sending the patient report to patient via email
        template_id = self.env.ref('hospital_management.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    # Set doctor gender according to its Id
    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    # Set Validation error if age is less
    @api.constrains('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age <= 5:
                raise ValidationError(_("Age Must be 6 or greater"))

    # select field for patient age(major minor)
    @api.depends('patient_age')
    def set_age_group(self):
        if self.patient_age < 18:
            self.age_group = 'minor'
        else:
            self.age_group = 'major'

    # this api is to open appointments of specific patient
    def open_patient_appointment(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    # This api counts the total number of appointments
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    # this api is for sequence
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
            result = super(HospitalPatient, self).create(vals)
            return result

    # this is for scheduling a job
    @api.model
    def test_cron_job(self):
        print("Working")

    # this api is for the print report through button

    def action_print_report(self):
        # Add code here
        return self.env.ref('hospital_management.report_patient_card').report_action(self)

    def print_report_excel(self):
        return self.env.ref('hospital_management.xlsx_report_patient_card').report_action(self)

#Server actions through menuitem
    def action_patients(self):
        return {
            'name': _('Patient Server Action'),
            'domain': [],
            'view_type': 'form',
            'res_model': 'hospital.patient',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

# this button is for delete record thorigh code
# @api.model
# def delete_record(self):
#     # Add code here
#     for rec in self:
#         rec.patient_id.unlink()
