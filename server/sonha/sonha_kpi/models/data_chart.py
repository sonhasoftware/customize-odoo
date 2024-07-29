from odoo import models, fields, api


class DataChart(models.Model):
    _name = 'data.chart'
    _description = 'Data Chart'

    department_id = fields.Many2one('hr.department', string='Phòng ban', required=True)
    progress = fields.Float(string='Tiến độ thực hiện năm (%)')
    work_volume = fields.Float(string='Khối lượng công việc thực hiện (%)')
    kpi_plan = fields.Float(string='KPI kế hoạch (%)')
    kpi_achieved = fields.Float(string='KPI thực hiện (%)')
    compliance_score = fields.Float(string='Điểm chấp hành (%)')
    improvement_score = fields.Float(string='Điểm cải tiến (%)')
    total_score = fields.Float(string='Tổng điểm')
    rating = fields.Selection([
        ('excellent', 'Xuất sắc'),
        ('good', 'Tốt'),
        ('average', 'Khá'),
        ('poor', 'Yếu')
    ], string='Xếp loại')