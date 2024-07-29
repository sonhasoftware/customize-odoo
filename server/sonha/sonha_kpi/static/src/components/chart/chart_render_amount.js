/** @odoo-module **/

import { loadJS } from '@web/core/assets';

const { Component, useState, onWillStart, useRef, onMounted } = owl;

export class RatingAmountChartRenderer extends Component {
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
      const ratingAmountData = [];

      this.state.data.forEach(item => {
        labels.push(item.department);
        ratingAmountData.push(item.rating_amount);
      });

      this.render(this.state.title, labels, ratingAmountData);
    });
  }

  render(title, labels, ratingAmountData) {
    new Chart(this.chartRef.el, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: title,
            data: ratingAmountData,
            backgroundColor: 'rgb(0, 0, 255)',
            borderColor: 'rgb(0, 0, 255)',
            borderWidth: 1,
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
        plugins: {
          datalabels: {
            display: true, // Hiển thị số trên cột
            color: '#000', // Màu sắc của số
            anchor: 'center', // Vị trí của số
            align: 'center', // Căn chỉnh số
            formatter: (value) => value + '%'
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Phòng ban' // Tiêu đề trục x
            }
          },
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Số lượng đánh giá'
            }
          }
        }
      },
      plugins: [ChartDataLabels]
    });
  }
}

RatingAmountChartRenderer.template = 'owl.RatingAmountChartRenderer'; // Đảm bảo định nghĩa template mới
