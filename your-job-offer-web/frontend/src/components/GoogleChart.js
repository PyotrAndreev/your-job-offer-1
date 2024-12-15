import { defineComponent, h } from 'vue';

import { GChart } from 'vue-google-charts';

export const type = 'AreaChart';

export const data = [
  ['Task', 'H'],
  ['Work', 11],
  ['Eat', 2],
  ['Commute', 2],
  ['Watch TV', 2],
  ['Sleep', 7],
];

export const options = {
//   title: 'My Daily Activities',
//   width: 800,
//   height: 600,
  colors: ['#6ea8fe', '#3d8bfd', '#0d6efd', '#0a58ca', '#084298']
};

export default defineComponent({
  name: 'GoogleChart',
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
