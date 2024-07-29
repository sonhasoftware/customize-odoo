from odoo import http
from odoo.http import request

class ColumnChartController(http.Controller):

    @http.route('/my_module/column_chart', auth='user', type='http')
    def column_chart(self, **kw):
        DataBI = request.env['data.bi']
        data = DataBI.search([])  # Lấy tất cả dữ liệu từ mô hình data.bi

        chart_data = [{
            'date': record.date,
            'quanty': record.quanty,
        } for record in data]

        return request.render('my_module.column_chart_template', {
            'chart_data': chart_data,
        })
