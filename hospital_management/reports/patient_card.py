from odoo import models, fields, api, _


class PatientCardReport(models.Model):
    _name = 'report.hospital_management.report_patient'
    _description = 'Patient Report Card'

    # This api is to get record of other table to print on report
    @api.model
    def _get_report_values(self, docids, data=None):
        print("yes entered here")
        docs = self.env['hospital.patient'].browse(docids[0])
        appointments = self.env['hospital.appointment'].search([('patient_id', '=', docids[0])])
        appointment_list = []
        for app in appointments:
            vals = {
                'name': app.name,
                'notes': app.notes,
                'appointment_date': app.appointment_date,
                # 'doctor_id': app.doctor_id
            }
            appointment_list.append(vals)

        return {
            'doc_model': 'hospital.patient',
            'docs': docs,
            'appointment_list': appointment_list,
        }

    # print('appointments', appointments)
    # print('appointment_list', appointment_list)
