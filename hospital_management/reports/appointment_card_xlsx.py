from odoo import fields, models, api, _


class AppointmentCardXlsx(models.AbstractModel):
    _name = 'report.hospital_management.report_appointment_xlsx'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_appointment_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter', })
        sheet = workbook.add_worksheet('Appointment Card')
        sheet.write(2, 2, 'Patient Name', format1)
        sheet.write(2, 3, lines.patient_id, format2)
        sheet.write(3, 2, 'Doctor', format1)
        sheet.write(3, 3, lines.doctor_id, format2)
