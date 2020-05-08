from pytz import utc

from odoo import models, fields, api, _


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    

    @api.multi
    def _get_work_days_data(self, from_datetime, to_datetime, compute_leaves=True, calendar=None, domain=None):
        """
            By default the resource calendar is used, but it can be
            changed using the `calendar` argument.
            `domain` is used in order to recognise the leaves to take,
            None means default value ('time_type', '=', 'leave')
            Returns a dict {'days': n, 'hours': h} containing the
            quantity of working time expressed as days and as hours.
        """
        resource = self.resource_id
        calendar = calendar or self.resource_calendar_id

        # naive datetimes are made explicit in UTC
        from_datetime = timezone_datetime(from_datetime)
        to_datetime = timezone_datetime(to_datetime)

        day_total = calendar._get_day_total(from_datetime, to_datetime, resource)

        # actual hours per day
        if compute_leaves:
            intervals = calendar._work_intervals(from_datetime, to_datetime, resource, domain)
        else:
            intervals = calendar._attendance_intervals(from_datetime, to_datetime, resource)

        return calendar._get_days_data(intervals, day_total)

class ResourceCalendarInherit(models.Model):
    _inherit = 'resource.calendar'


@api.multi
def get_work_hours_count(self, start_dt, end_dt, compute_leaves=True, domain=None):
    """
        `compute_leaves` controls whether or not this method is taking into
        account the global leaves.
        `domain` controls the way leaves are recognized.
        None means default value ('time_type', '=', 'leave')
        Counts the number of work hours between two datetimes.
    """
    # Set timezone in UTC if no timezone is explicitly given
    if not start_dt.tzinfo:
        start_dt = start_dt.replace(tzinfo=utc)
    if not end_dt.tzinfo:
        end_dt = end_dt.replace(tzinfo=utc)

    if compute_leaves:
        intervals = self._work_intervals(start_dt, end_dt, domain=domain)
    else:
        intervals = self._attendance_intervals(start_dt, end_dt)
        return sum(
            (stop - start).total_seconds() / 3600
            for start, stop, meta in intervals
        )


class ResourceInherit(models.Model):
    _inherit = 'resource.resource'


@api.multi
def _get_work_interval(self, start, end):
    """ Return interval's start datetime for interval closest to start. And interval's end datetime for interval closest to end.
        If none is found return None
        Note: this method is used in enterprise (forecast and planning_old)
        :start: datetime
        :end: datetime
        :return: (datetime|None, datetime|None)
    """
    start_datetime = timezone_datetime(start)
    end_datetime = timezone_datetime(end)
    resource_mapping = {}
    for resource in self:
        work_intervals = sorted(
            resource.calendar_id._work_intervals(start_datetime, end_datetime, resource),
            key=lambda x: x[0]
        )
        if work_intervals:
            resource_mapping[resource.id] = (
                work_intervals[0][0].astimezone(utc), work_intervals[-1][1].astimezone(utc))
        else:
            resource_mapping[resource.id] = (None, None)
    return resource_mapping


class ResourceMixinInherit(models.Model):
    _inherit = 'resource.mixin'


ROUNDING_FACTOR = 16


@api.multi
def timezone_datetime(time):
    if not time.tzinfo:
        time = time.replace(tzinfo=utc)
    return time
