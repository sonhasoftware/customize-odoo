/** @odoo-module **/

import { loadJS } from '@web/core/assets';

const { Component, useState, onWillStart, useRef, onMounted } = owl;

export class KPIAmountChartRenderer extends Component {
  setup() {
    this.chartRef = useRef('chart');
    this.state = useState({
      title: this.props.title,
      data: this.props.data
    });

    onWillStart(async () => {
      await loadJS('https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js');
      await loadJS('https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.0.0/dist/chartjs-plugin-datalabels.min.js');
    });

    onMounted(() => {
      const labels = [];
      const kpiData = [];
      const kpiPlanData = [];

      this.state.data.forEach(item => {
        labels.push(item.department);
        kpiData.push(item.rating_amount);
        kpiPlanData.push(item.result_amount);
      });

      this.render(this.state.title, labels, kpiData, kpiPlanData);
    });
  }

  render(title, labels, kpiData, kpiPlanData) {
    new Chart(this.chartRef.el, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: '% TH khối lượng công việc',
            data: kpiData,
            backgroundColor: '#1E90FF',
            borderColor: '#1E90FF',
            borderWidth: 1,
            barThickness: 15,
            datalabels: {
              anchor: 'center',
              align: 'center',
              formatter: (value) => value + '%',
              color: 'white',
              font: {
                weight: 'bold'
              }
            }
          },
          {
            label: '% thực hiện theo các tiêu chí',
            data: kpiPlanData,
            backgroundColor: '#00008B',
            borderColor: '#00008B',
            borderWidth: 1,
            barThickness: 15,
            datalabels: {
              anchor: 'center',
              align: 'center',
              formatter: (value) => value + '%',
              color: 'white',
              font: {
                weight: 'bold'
              }
            }
          }
        ]
      },
      options: {
        indexAxis: 'y', // Chuyển trục x thành trục y
        scales: {
          x: {
            beginAtZero: true,
            stacked: false // Đảm bảo rằng thanh không xếp chồng lên nhau
          },
          y: {
            stacked: false // Đảm bảo rằng thanh không xếp chồng lên nhau
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                return context.dataset.label + ': ' + context.raw + '%';
              }
            }
          },
          datalabels: {
            display: true, // Hiển thị số trên cột
            color: '#000', // Màu sắc của số
            anchor: 'center', // Vị trí của số
            align: 'center', // Căn chỉnh số
            formatter: (value) => value + '%'
          }
        }
      },
      plugins: [ChartDataLabels]
    });
  }
}

KPIAmountChartRenderer.template = 'owl.KPIAmountChartRenderer';
