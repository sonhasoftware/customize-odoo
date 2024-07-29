/** @odoo-module */

import { Component } from 'web';
import { qweb } from 'web.core';
import Chart from 'chart.js/auto';

var ColumnChartWidget = Component.extend({
    template: 'ColumnChartWidget',

    // Định nghĩa sự kiện nếu có
    events: {
        // Định nghĩa sự kiện tại đây nếu cần
    },

    init: function (parent, data) {
        this._super.apply(this, arguments);
        this.chartData = data.chartData || [];
    },

    start: function () {
        console.log('Bắt đầu khởi tạo component'); // Debug statement
        this._renderChart();
    },

    _renderChart: function () {
        console.log('Đang vẽ biểu đồ'); // Debug statement

        // Kiểm tra xem phần tử canvas có tồn tại không
        var canvasElements = this.$('canvas');
        if (canvasElements.length === 0) {
            console.error('Không tìm thấy phần tử canvas');
            return;
        }

        var ctx = canvasElements[0].getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: this.chartData.map(item => item.date),
                datasets: [{
                    label: 'Số lượng',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    data: this.chartData.map(item => item.quantity), // Sửa lỗi chính tả 'quanty' thành 'quantity'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    xAxes: [{
                        ticks: {
                            autoSkip: false,
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero: true,
                        }
                    }]
                }
            }
        });
    }
});

return ColumnChartWidget;
