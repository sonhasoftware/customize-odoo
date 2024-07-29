/** @odoo-module **/

import { loadJS } from '@web/core/assets';

const { Component, useState, onWillStart, useRef, onMounted } = owl;

export class OwlChartRenderer extends Component {
  setup() {
    this.chartRef = useRef('chart');
    this.state = useState({
      title: this.props.title,
      type: this.props.type || 'bar',
      data: this.props.data
    });

    onWillStart(async () => {
      await loadJS('https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js');
      await loadJS('https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0/dist/chartjs-plugin-datalabels.min.js');
    });

    onMounted(() => {
      const labels = [];
      const completeData = [];
      const unfulfilledData = [];
      const processingData = [];

      if (Array.isArray(this.state.data)) {
        this.state.data.forEach(item => {
          labels.push(item.department);
          completeData.push(item.complete);
          unfulfilledData.push(item.unfulfilled);
          processingData.push(item.processing);
        });
      } else {
        console.error('Dữ liệu không phải là mảng:', this.state.data);
      }

      this.render(this.state.title, labels, completeData, unfulfilledData, processingData, this.state.type);
    });
  }

  render(title, labels, completeData, unfulfilledData, processingData, type) {
    new Chart(this.chartRef.el, {
      type,
      data: {
        labels,
        datasets: [
          {
            label: 'Hoàn thành',
            data: completeData,
            backgroundColor: 'rgb(106, 90, 205)', // Màu nền
            borderColor: 'rgb(106, 90, 205)',
            borderWidth: 1,
            datalabels: {
              anchor: 'center',
              align: 'center',
              formatter: (value, context) => value + "%",
              color: 'white',
              font: {
                weight: 'bold'
              }
            }
          },
          {
            label: 'Chưa thực hiện',
            data: unfulfilledData,
            backgroundColor: 'rgba(255, 99, 71, 0.5)', // Màu nền
            borderColor: 'rgba(255, 99, 71, 0.5)',
            borderWidth: 1,
            datalabels: {
              anchor: 'center',
              align: 'center',
              formatter: (value, context) => value + "%",
              color: 'white',
              font: {
                weight: 'bold'
              }
            }
          },
          {
            label: 'Đang thực hiện',
            data: processingData,
            backgroundColor: 'rgb(255, 165, 0)', // Màu nền
            borderColor: 'rgb(255, 165, 0)',
            borderWidth: 1,
            datalabels: {
              anchor: 'center',
              align: 'center',
              formatter: (value, context) => value + "%",
              color: 'white',
              font: {
                weight: 'bold'
              }
            }
          }
        ]
      },
      options: {
        plugins: {
          datalabels: {
            display: function(context) {
              return context.dataset.data[context.dataIndex] > 0; // Chỉ hiển thị nhãn nếu giá trị > 0
            }
          }
        },
        scales: {
          x: {
            stacked: true
          },
          y: {
            stacked: true,
            beginAtZero: true
          }
        }
      },
      plugins: [ChartDataLabels]
    });
  }
}

OwlChartRenderer.template = 'owl.OwlChartRenderer';
