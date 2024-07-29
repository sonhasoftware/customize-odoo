/** @odoo-module **/

import { registry } from '@web/core/registry';
import { useService } from '@web/core/utils/hooks';
import { OwlChartRenderer } from './chart/chart_renderer';
import { RatingAmountChartRenderer } from './chart/chart_render_amount';
import { RatioKPIChartRenderer } from './chart/chart_render_ratio_kpi';
import { CriteriaPointsChartRenderer } from './chart/criteria_points_render';
import { KPIPlanChartRenderer } from './chart/chart_render_kpi_plan';
import { KPIAmountChartRenderer } from './chart/chart_render_kpi_amount';

const { Component, useState, onWillStart } = owl;

export class OwlGreetDashboard extends Component {
  setup() {
    this.state = useState({
      title: 'Tổng hợp KPI theo phòng ban',
      kpiData: [],
      ratingAmountData: [],
      ratioKPIData: [],
      criteriaPointsData: [],
      kpiPlan: [],
      kpiAmount: [],
    });

    this.orm = useService('orm');

    onWillStart(async () => {
      const data = await this.getKpiData();
      this.state.kpiData = data;
      this.state.ratingAmountData = data;
      this.state.ratioKPIData = data;
      this.state.criteriaPointsData = data;
      this.state.kpiPlan = data;
      this.state.kpiAmount = data;
    });
  }

  async getKpiData() {
    const response = await fetch('/check_method_get');
    const data = await response.json();
    return data;
  }
}

OwlGreetDashboard.template = 'owl.OwlGreetDashboard';
OwlGreetDashboard.components = { OwlChartRenderer, RatingAmountChartRenderer, RatioKPIChartRenderer, CriteriaPointsChartRenderer, KPIPlanChartRenderer, KPIAmountChartRenderer };

registry.category('actions').add('owl.greet_dashboard', OwlGreetDashboard);
