from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ConfigColumn(models.Model):
    _name = 'config.column'

    operation = fields.Selection([
        ('add', 'Cộng'),
        ('subtract', 'Trừ'),
        ('multiply', 'Nhân'),
        ('divide', 'Chia')
    ], string='Operation', required=True)
    field1_id = fields.Many2one('ir.model.fields', string='Field 1', domain=[('model_id', '=', 'sonha.kpi.rel')], ondelete='cascade')
    field2_id = fields.Many2one('ir.model.fields', string='Field 2', domain=[('model_id', '=', 'sonha.kpi.rel')],  ondelete='cascade')
    result_field_id = fields.Many2one('ir.model.fields', string='Result Field', domain=[('model_id', '=', 'sonha.kpi.rel')], ondelete='cascade')

    department_id = fields.Many2one('hr.department', string="Phòng ban")

    number = fields.Integer('Số')


