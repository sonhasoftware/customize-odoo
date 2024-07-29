/** @odoo-module **/

import { loadJS } from '@web/core/assets';

const { Component, useState, onWillStart, useRef, onMounted } = owl;

export class CriteriaPointsChartRenderer extends Component {
  setup() {
    this.chartRef = useRef('chart');
    this.state = useState({
      title: this.props.title,
      data: this.props.data || [] // Đảm bảo dữ liệu là mảng, nếu không có dữ liệu thì mặc định là mảng rỗng
    });

    onWillStart(async () => {
      await loadJS('https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js');
    });

    onMounted(() => {
      const labels = [];
      const amountData = [];
      const matterData = [];
      const regulationsData = [];
      const initiativeData = [];
      const progressPointsData = [];
      const totalData = [];

      // Kiểm tra xem dữ liệu có phải là một mảng và không rỗng
      if (Array.isArray(this.state.data) && this.state.data.length) {
        this.state.data.forEach(item => {
          labels.push(item.department);
          amountData.push(item.amount);
          matterData.push(item.matter);
          regulationsData.push(item.regulations);
          initiativeData.push(item.initiative);
          progressPointsData.push(item.progress_points);
          totalData.push(item.total);
        });
      }

      this.renderChart(labels, amountData, matterData, regulationsData, initiativeData, progressPointsData, totalData);
    });
  }

  renderChart(labels, amountData, matterData, regulationsData, initiativeData, progressPointsData, totalData) {
    new Chart(this.chartRef.el, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Khối lượng công việc',
            data: amountData,
            backgroundColor: '#6495ED',
            borderColor: '#6495ED',
            borderWidth: 1
          },
          {
            label: 'Chất lượng CV TH',
            data: matterData,
            backgroundColor: '#B8860B',
            borderColor: '#B8860B',
            borderWidth: 1
          },
          {
            label: 'Chấp hành nội quy',
            data: regulationsData,
            backgroundColor: '#FFE4C4',
            borderColor: '#FFE4C4',
            borderWidth: 1
          },
          {
            label: 'Cải tiến, đề xuất, sáng kiến',
            data: initiativeData,
            backgroundColor: '#A52A2A',
            borderColor: '#A52A2A',
            borderWidth: 1
          },
          {
            label: 'Điểm tiến bộ',
            data: progressPointsData,
            backgroundColor: '#FF00FF',
            borderColor: '#FF00FF',
            borderWidth: 1
          },
          {
            label: 'Tổng điểm',
            data: totalData,
            backgroundColor: '#00008B',
            borderColor: '#00008B',
            borderWidth: 1
          }
        ]
      },
      options: {
        scales: {
          x: {
            stacked: true // Kích hoạt tính năng xếp chồng cho trục x
          },
          y: {
            stacked: true, // Kích hoạt tính năng xếp chồng cho trục y
            beginAtZero: true
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.dataset.label + ': ' + context.raw;
              }
            }
          }
        }
      }
    });
  }
}

CriteriaPointsChartRenderer.template = 'owl.CriteriaPointsChartRenderer';
