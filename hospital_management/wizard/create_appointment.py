from odoo import models, fields, api, _


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'
    _description = 'Create Appointment Wizard'

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    appointment_date = fields.Date(string="Appointment Date")

    # this api is for create button

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
            'appointment_date': self.appointment_date
        }
        self.patient_id.message_post(body="Appointment created", subject="Appointment")
        new_appointment = self.env['hospital.appointment'].create(vals)
        # if want to open form in edit mode then remove the
        # context = dict(self.env.context)
        # context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.appointment',
                'res_id': new_appointment.id,
                # 'context': context
                }

    # this api is for get data from data base

    def get_method(self):
        appointments = self.env['hospital.appointment'].search([])
        print('appointments', appointments)
        for rec in appointments:
            print("Appointment Name", rec.name)
        return {
            "type": "ir.actions.do_nothing"
        }

    # print report through wizard
    def print_report(self):
        print("kkk--->", self.read()[0])
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }
        print("Data", data)
        return self.env.ref('hospital_management.report_appointment').with_context(landscape=True).report_action(self,
                                                                                                                 data=data)

        # if data['form']['patient_id']:
        #     selected_patient = data['form']['patient_id'][0]
        #     appointments = self.env['hospital.appointment'].search([('patient_id', '=', selected_patient)])
        # else:
        #     appointments = self.env['hospital.appointment'].search([])
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name': app.name,
        #         'notes': app.notes,
        #         'appointment_date': app.appointment_date,
        #         'doctor_id': app.doctor_id,
        #     }
        #     appointment_list.append(vals)
        # # print("appointments", appointments)
        # data['appointments'] = appointment_list
