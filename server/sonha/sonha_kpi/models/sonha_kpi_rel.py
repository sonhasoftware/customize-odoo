from odoo import api, fields, models, _
import pandas as pd
from odoo.exceptions import UserError, ValidationError


class SonHaKPIRel(models.Model):
    _name = 'sonha.kpi.rel'

    kpi_id = fields.Many2one('sonha.kpi')
    content = fields.Char('Nội dung')
    ti_trong = fields.Integer('Tỉ trọng')
    diem_chuan = fields.Integer('Điểm chuẩn')
    description = fields.Text('Mô tả đánh giá')
    Chi_tieu_giao = fields.Integer('Chỉ tiêu giao')
    ket_qua_dat = fields.Integer('Kết quả đạt')
    diem_dat = fields.Integer('Điểm đạt')
    diem_quy_doi = fields.Float('Điểm quy đổi tỷ trọng')
    diem_tien_bo = fields.Float('Điểm tiến bộ')
    diem = fields.Float('Điểm')
    Xep_loai = fields.Char('Xếp loại tháng')
    note = fields.Text('Ghi chú')
    date_kpi = fields.Date('Ngày')
    calculated = fields.Boolean(string='Calculated', default=False)

    def calculate_fields(self, record):
        configs = self.env['config.column'].sudo().search([])
        configs = configs.filtered(lambda x: x.department_id.id in record.kpi_id.employee_id.department_ids.ids)

        data_by_so = {}
        for rec in configs:
            so = rec.number
            if so not in data_by_so:
                data_by_so[so] = []
            data_by_so[so].append({
                'result_field': rec.result_field_id.name,
                'field1': rec.field1_id.name,
                'operation': rec.operation,
                'field2': rec.field2_id.name if rec.field2_id else None
            })

        # Dictionary tạm thời để lưu trữ các công thức từng nhóm
        formulas = {}

        # Xử lý từng nhóm để xây dựng công thức hoàn chỉnh
        for so, data in data_by_so.items():
            formula_parts = []
            for item in data:
                field1 = item['field1']
                operation = item['operation']
                field2 = item['field2']

                if operation == "add":
                    operator = "+"
                elif operation == "multiply":
                    operator = "*"
                elif operation == "divide":
                    operator = "/"
                else:
                    operator = "-"  # Xử lý các phép toán khác nếu cần

                if field2:
                    formula_part = f"({field1} {operator} {field2})"
                else:
                    formula_part = f"{field1} {operator}"

                formula_parts.append(formula_part)

            # Kết nối các phần của công thức lại với nhau
            formulas[so] = " ".join(formula_parts).strip(" +*-/")

        # Tính toán và ghi kết quả vào các trường result_field tương ứng
        results = {}
        for so, formula in formulas.items():
            try:
                local_vars = {field: getattr(record, field, 0) for field in record._fields}
                result = eval(formula, {"__builtins__": None}, local_vars)
                result_field = data_by_so[so][0]['result_field']
                results[result_field] = result
            except Exception as e:
                # Xử lý các lỗi tính toán (nếu có)
                raise ValueError(f"Error evaluating formula {formula}: {e}")

        results['calculated'] = True
        record.write(results)

    def calculate_it_fields(self, record):
        config = self.env['config.recipe'].search([])
        results = {}
        for r in config:
            str = r.recipe
            expression = str.split()
            field = r.result_field_id.name
            recipe = ""
            for item in expression:
                if len(item) > 1:
                    recipe += "record." + item
                else:
                    recipe += item
            recipe = eval(recipe)
            results[field] = recipe

        results['calculated'] = True
        record.write(results)

    @api.model
    def create(self, vals):
        record = super(SonHaKPIRel, self).create(vals)
        configs = self.env['config.column'].sudo().search([])
        configs = configs.filtered(lambda x: x.department_id.id in record.kpi_id.employee_id.department_ids.ids)
        if not configs and 'calculated' not in vals:
            self.calculate_it_fields(self)
        if configs and 'calculated' not in vals:
            self.calculate_fields(record)
        return record

    def write(self, vals):
        res = super(SonHaKPIRel, self).write(vals)
        configs = self.env['config.column'].sudo().search([])
        configs = configs.filtered(lambda x: x.department_id.id in self.kpi_id.employee_id.department_ids.ids)
        if not configs and 'calculated' not in vals:
            self.calculate_it_fields(self)
        if configs and 'calculated' not in vals:
            self.calculate_fields(self)
        return res
