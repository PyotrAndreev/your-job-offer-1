import { defineComponent, h } from 'vue';

import { GChart } from 'vue-google-charts';

export const type = 'PieChart';

export const data = [
  ['Applications', 'Progress'],
  ['Offers found', 2],
  ['Offers to find', 8],
];

export const options = {
  legend: {position: 'bottom'},
  colors: ['#6ea8fe', '#3d8bfd', '#0d6efd', '#0a58ca', '#084298']
};

export default defineComponent({
  name: 'PieChart',
  components: {
    GChart,
  },
  setup() {
    return () =>
      h(GChart, {
        data,
        options,
        type,
      });
  },
});
