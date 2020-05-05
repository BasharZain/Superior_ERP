from odoo import api, fields, models


class AppointmentReport(models.AbstractModel):
    _name = 'report.hospital_management.appointment_report'
    _description = 'Appointment Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        if data['form']['patient_id']:
            appointments = self.env['hospital.appointment'].search([('patient_id', '=', data['form']['patient_id'][0])])
        else:
            appointments = self.env['hospital.appointment'].search([])
        appointments_list = []
        for app in appointments:
            vals = {
                'name': app.name,
                'notes': app.notes,
                'state':app.state,
                'doctor_id': app.doctor_id,
                'patient_id': app.patient_id,
            }
            appointments_list.append(vals)
            return {
                'doc_model': 'hospital.patient',
                'appointments': appointments
            }
