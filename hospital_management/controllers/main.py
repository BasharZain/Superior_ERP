from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
# This is for inherit controller of another module
from odoo.odoo import SUPERUSER_ID
from odoo.exceptions import AccessError, MissingError
from odoo import fields, _
from odoo.tools import consteq
from odoo.odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class WebsiteSaleDInherit(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        response = super(WebsiteSaleDInherit, self).shop(page=0, category=None, search='', ppg=False, **post)
        print("Inherited", response)
        return response


class Hospital(http.Controller):

    @http.route(['/hospital/patient/'], type='http', website=True, auth='public')
    def hospital_patient(self, **kw):
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render("hospital_management.patient_page", {
            'patients': patients,
        })

    @http.route(['/hospital/patient/appointments/<int:patient_id>'], type='http', website=True,
                auth='public')
    def patient_appointments(self, patient_id, access_token=None, **rec):
        values = dict(**rec)
        if ['rec']:
            print("rec....", rec)

        appointments = request.env['hospital.appointment'].sudo().search([('patient_id', '=', patient_id)])
        return request.render("hospital_management.patient_appointment", {'appointments': appointments, })

    @http.route('/patient_form/', type="http", auth="public", website=True)
    def patient_form(self, **kw):
        doctor_rec = request.env['hospital.doctor'].sudo().search([])
        return http.request.render('hospital_management.create_patient', {'doctor_rec': doctor_rec})

    @http.route('/create/patient/', type="http", auth="public", website=True)
    def create_patient(self, **kw):
        request.env['hospital.patient'].sudo().create(kw)
        return request.render("hospital_management.patient_thanks", {})

# @http.route(['/hospital/patient/appointments/<int:patient_id>'], type='http', methods=['GET'], website=True,
#             auth='public')
# def patient_appointments(self, patient_id, **rec):
#     values = dict(**rec)
#     if ['rec']:
#         print("rec....", rec)
#         appointments = request.env['hospital.appointment'].sudo().browse(patient_id)
#         # appointments = request.env['hospital.appointment'].sudo().search([('patient_id', '=', patients)])
#     return request.render("hospital_management.patient_appointment", {
#         'appointments': appointments,
#
#     })
#
# @http.route('/update_patient', type='json', auth='user')
# def update_patient(self, **rec):
#     if request.jsonrequest:
#         if rec['id']:
#             print("rec...", rec)
#             patient = request.env['hospital.patient'].sudo().search([('id', '=', rec['id'])])
#             if patient:
#                 patient.sudo().write(rec)
#             args = {'success': True, 'message': 'Patient Updated'}
#     return args
#
# @http.route('/create_patient', type='json', auth='user')
# def create_patient(self, **rec):
#     if request.jsonrequest:
#         print("rec", rec)
#         if rec['name']:
#             vals = {
#                 'patient_name': rec['name'],
#                 'email_id': rec['email_id']
#             }
#             new_patient = request.env['hospital.patient'].sudo().create(vals)
#             print("New Patient Is", new_patient)
#             args = {'success': True, 'message': 'Success', 'id': new_patient.id}
#     return args
#
# @http.route('/get_patients', type='json', auth='user')
# def get_patients(self):
#     print("Yes here entered")
#     patients_rec = request.env['hospital.patient'].search([])
#     patients = []
#     for rec in patients_rec:
#         vals = {
#             'id': rec.id,
#             'name': rec.patient_name,
#             'sequence': rec.name_seq,
#         }
#         patients.append(vals)
#     print("Patient List--->", patients)
#     data = {'status': 200, 'response': patients, 'message': 'Done All Patients Returned'}
#     return data
