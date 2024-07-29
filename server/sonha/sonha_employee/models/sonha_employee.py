from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SonHaEmployee(models.Model):
    _inherit = 'hr.employee'

    list_employee = fields.Many2many('hr.employee', 'ir_employee_group_rel',
                                     'employee_group_rel', 'employee_rel',
                                     string='List Staff', compute="filter_list_employee", store=True, readonly=False)

    lower_grade = fields.Many2many('hr.employee', 'ir_lower_grade_id_rel',
                                   'lower_grade_id_rel', 'lower_grade_id',
                                    string="Lower Grade")

    kpi = fields.Many2many('hr.employee', 'ir_kpi_id_rel',
                           'kpi_id_rel', 'kpi_id',
                           string="Edit KPI")

    department_ids = fields.Many2many('hr.department', 'ir_department_ids_rel',
                                      'department_ids_rel', 'department_ids',
                                      string="Department")

    level = fields.Selection([
        ('N0', 'N0'),
        ('N1', 'N1'),
        ('N2', 'N2'),
        ('N3', 'N3'),
        ('N4', 'N4'),
        ('N5', 'N5'),
    ], string='Level')

    date = fields.Date('Ngày')
    number = fields.Integer('Số')

    @api.onchange('list_employee')
    def _onchange_list_employee(self):
        if self.list_employee:
            return {'domain': {'kpi': [('id', 'in', self.list_employee.ids)]}}
        else:
            self.filter_list_employee()
            return {'domain': {'kpi': []}}

    @api.onchange('list_employee')
    def filter_list_employee(self):
        for r in self:
            if len(r.lower_grade) > 0:
                list_emp = []
                for item in r.lower_grade:
                    list_emp.append(item.id)
                    list_emp.append(item.list_employee.ids)
                flattened_list = [item for sublist in list_emp for item in
                                  (sublist if isinstance(sublist, list) else [sublist])]
                r.list_employee = flattened_list
            else:
                r.list_employee = None