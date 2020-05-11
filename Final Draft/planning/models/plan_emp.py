from odoo import models,fields,api

class EmployeePlan(models.Model):
    _inherit = 'hr.employee'

    emp_plan_count = fields.Integer(compute='_compute_emp_plan_count', string='Advance Salary Count')

    def _compute_emp_plan_count(self):
        for rec in self:
            rec.emp_plan_count = self.env['planning.slot'].search_count([('employee_id', '=', rec.id)])
