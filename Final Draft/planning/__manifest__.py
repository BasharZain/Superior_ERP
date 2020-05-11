# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Planning",
    'summary': """Manage your employees' schedule""",
    'description': """
    Schedule your teams and employees with shift.
    """,
    'category': 'Human Resources/Planning',
    'version': '1.0',
    'depends': ['hr', 'web_timeline', 'web_gantt'],
    'data': [
        #'views/mail_activity_views.xml',
        #'views/mail_data.xml',
        'security/planning_security.xml',
        'security/ir.model.access.csv',
        # 'wizard/planning_send_views.xml',
        'views/assets.xml',
        'views/hr_views.xml',
        'report/planning_report_views.xml',
        'views/planning_template_views.xml',
        'views/planning_views.xml',
        'views/res_config_settings_views.xml',
        'views/planning_templates.xml',
        'views/report_views.xml',
        'views/hr_emp.xml',
        'data/planning_cron.xml',
        'data/mail_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    'qweb': [
        'static/src/xml/field_colorpicker.xml',
    ]
}
