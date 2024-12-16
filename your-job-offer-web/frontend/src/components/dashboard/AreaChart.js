import { defineComponent, h } from 'vue';

import { GChart } from 'vue-google-charts';

export const type = 'AreaChart';

export const data = [
  ['Applications', 'X'],
  ['August', 2],
  ['September', 4],
  ['Ocotber', 8],
  ['November', 5],
  ['December', 12],
];

export const options = {
//   title: 'My Daily Activities',
//   width: 800,
//   height: 600,

  colors: ['#6ea8fe', '#3d8bfd', '#0d6efd', '#0a58ca', '#084298']
};

export default defineComponent({
  name: 'AreaChart',
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
