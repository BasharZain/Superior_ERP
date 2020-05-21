from odoo import models, fields, api, tools


class CustomReport(models.Model):
    _name = 'schedule.report'
    _description = 'Actual vs Planned Report'
    _auto = False

    DATETIME_FORMAT = "%m-%d-%Y %H:%M:%S"
    active = fields.Boolean('active', default=True, store=True)
    id = fields.Integer('id', store=True)
    check_in = fields.Datetime(string='Check in')
    check_out = fields.Datetime(string='Check out')
    name = fields.Char(string ='Employee Name')
    start_datetime = fields.Datetime(string='Scheduled Start')
    end_datetime = fields.Datetime(string='Scheduled End')
    allocated_hours = fields.Float(string='Scheduled Hours')
    worked_hours = fields.Float(string='Worked Hours')
    late_min = fields.Datetime(string="Maximum Start Time")

    new_late = fields.Char(string='Late Minutes')
    extra_time = fields.Char(string='OverTime')



    @api.model_cr
    def init(self):
        """ Event Question main report """
        tools.drop_view_if_exists(self._cr, 'schedule_report')
        self._cr.execute(""" CREATE VIEW schedule_report AS (
           select 
           		a.id as id,
        active as active,
           a.check_in as check_in,
		a.worked_hours as worked_hours,
		a.check_out as check_out, 
		b.start_datetime as start_datetime, 
		b.end_datetime as end_datetime,
		b.allocated_hours as allocated_hours,
		b.date_field2 as late_min,
		c.name as name,
		age(a.check_in, b.date_field2) as new_late,
		SUM(a.worked_hours - b.allocated_hours) as extra_time

from hr_attendance as a

left join planning_slot as b

on to_char(a.check_in, 'YYYY/MM/DD') = to_char(b.start_datetime, 'YYYY/MM/DD')
and a.employee_id = b.employee_id

inner join hr_employee as c
on a.employee_id = c.id

Group By a.id,
        active,
           a.check_in,
		a.worked_hours,
		a.check_out, 
		b.start_datetime, 
		b.end_datetime,
		b.allocated_hours,
		b.date_field2,
		c.name 
            )""")



