from odoo import http
from odoo.http import request

import json


class DataChart(http.Controller):

    @http.route("/check_method_get", auth='none', type='http', method=['GET'])
    def check_method_get(self, **values):
        department_ids = request.env['hr.department'].sudo().search([])
        data = []
        for department_id in department_ids:
            complete, unfulfilled, processing = self.get_data_progress(department_id)
            rating_amount = self.rating_amount_work_performed(department_id)
            kpi_plan, kpi_perform = self.kpi_amount(department_id)
            amount, matter, regulations, initiative, progress_points, total = self.criteria_points(department_id)
            result_amount = self.result_amount(department_id)
            data.append({
                'department': department_id.name,
                'complete': round(complete, 2),
                'unfulfilled': round(unfulfilled, 2),
                'processing': round(processing, 2),
                'rating_amount': round(rating_amount, 2),
                'kpi_plan': round(kpi_plan, 2),
                'kpi_th': round(kpi_perform, 2),
                'amount': round(amount, 2),
                'matter': round(matter, 2),
                'regulations': round(regulations, 2),
                'initiative': round(initiative, 2),
                'progress_points': round(progress_points, 2),
                'total': round(total, 2),
                'result_amount': round(result_amount, 2),
            })
        return json.dumps(data)

    def get_data_progress(self, department_id):
        complete = 0
        unfulfilled = 0
        processing = 0
        data = request.env['sonha.kpi.year'].sudo().search([('department_id', '=', department_id.id)])
        data_dang_th = data.filtered(lambda x: x.dvdg_status == 'in_progres')
        data_ht = data.filtered(lambda x: x.dvdg_status == 'done')
        data_chua_th = data.filtered(lambda x: x.dvdg_status == 'draft')
        if data_ht:
            complete = sum(data_ht.mapped('dvdg_kpi')) * 100
        if data_dang_th:
            processing = sum(data_dang_th.mapped('dvdg_kpi')) * 100
        if data_chua_th:
            unfulfilled = 100 - complete - processing
        return complete, unfulfilled, processing

    def rating_amount_work_performed(self, department_id):
        data = request.env['sonha.kpi.month'].sudo().search([('department_id', '=', department_id.id)]).mapped('dv_amount_work')
        rating_amount = 0
        if data:
            rating_amount = (sum(data) / len(data)) * 100
        return rating_amount

    def kpi_amount(self, department_id):
        kpi_plan = 0
        kpi_perform = 0
        data_plan = request.env['sonha.kpi.year'].sudo().search([('department_id', '=', department_id.id)]).mapped('kpi_year')
        data_perform = request.env['sonha.kpi.year'].sudo().search([('department_id', '=', department_id.id)]).mapped('dvdg_kpi')
        if data_plan:
            kpi_plan = (sum(data_plan) / len(data_plan)) * 100
        if data_perform:
            kpi_perform = (sum(data_perform) / len(data_perform)) * 100
        return kpi_plan, kpi_perform

    def criteria_points(self, department_id):
        amount = 0
        matter = 0
        regulations = 0
        initiative = 0
        progress_points = 0

        data_amount = request.env['sonha.kpi.result.month'].sudo().search(
            [('department_id', '=', department_id.id)]).mapped('diem_dat_dv_amount_work')
        data_matter = request.env['sonha.kpi.result.month'].sudo().search(
            [('department_id', '=', department_id.id)]).mapped('diem_dat_dv_matter_work')
        data_regulations = request.env['sonha.kpi.result.month'].sudo().search(
            [('department_id', '=', department_id.id)]).mapped('diem_dat_dv_comply_regulations')
        data_initiative = request.env['sonha.kpi.result.month'].sudo().search(
            [('department_id', '=', department_id.id)]).mapped('diem_dat_dv_initiative')
        if data_amount:
            amount = sum(data_amount) / len(data_amount)
        if data_matter:
            matter = sum(data_matter) / len(data_matter)
        if data_regulations:
            regulations = sum(data_regulations) / len(data_regulations)
        if data_initiative:
            initiative = sum(data_initiative) / len(data_initiative)
        total = amount + matter + regulations + initiative
        return amount, matter, regulations, initiative, progress_points, total

    def result_amount(self,department_id):
        result_amount = 0
        data_result_amount = request.env['sonha.kpi.result.month'].sudo().search(
            [('department_id', '=', department_id.id)]).mapped('kq_hoan_thanh_amount_work')
        if data_result_amount:
            result_amount = (sum(data_result_amount) / len(data_result_amount)) * 100
        return result_amount
