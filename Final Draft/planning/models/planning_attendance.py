from odoo import models,api,fields

class PlanAttend(models.Model):
    _inherit = 'hr.attendance'

    attend_duration = fields.Float(compute='get_inside_calendar_duration',string='Duration')

    def get_inside_calendar_duration(self, planning, check_in, check_out):
        plan_attend = self.env['planning.slot']
        dayofweek = {'Monday': '0', 'Tuesday': '1', 'Wednesday': '2', 'Thursday': '3', 'Friday': '4', 'Saturday': '5',
                       'Sunday': '6'}
        day_id = check_in.strftime('%A')
        att_line_target = False
        in_duration = 0.0
        out_duration = 0.0
        if planning:
            for day in plan_attend.dayofweek:
                if str(day.dayofweek) == dayofweek[day_id]:
                    att_line_target = day

            if att_line_target:
                start_time = att_line_target.start_datetime
                end_time = att_line_target.end_datetime
                start1 = start_time
                check_in_time = self.convert_to_float(str(check_in.time()))
                check_out_time = self.convert_to_float(str(check_out.time()))

                if check_in_time >= start_time:
                    start1 = check_in_time
                else:
                    out_duration += start_time - check_in_time

                end1 = end_time
                if check_out_time <= end_time:
                    end1 = check_out_time
                else:
                    out_duration += check_out_time - end_time

                in_duration = end1 - start1

        return [in_duration, out_duration]