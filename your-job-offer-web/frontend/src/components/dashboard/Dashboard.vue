<template>
  <div class="p-4 bg-light">
    <h2 class="mb-4">Dashboard</h2>
    <div class="row g-4">
      <!-- Progress Card -->
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card p-3 text-center shadow-sm">
          <h5 class="card-title">Progress</h5>
          <!-- <GChart type="AreaChart" :data="chartData" :options="chartOptions" /> -->
          <GoogleChart />
        </div>
      </div>

      <!-- Offers Goal -->
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card p-3 text-center shadow-sm h-100">
          <h5 class="card-title">How many offers to find?</h5>
          <div
            class="d-flex align-items-center justify-content-center counter w-100"
          >
            <!-- Left Arrow Button -->
            <button class="btn btn-primary rounded-5" @click="decrementNumber">
              <font-awesome-icon :icon="['fas', 'angle-left']" />
            </button>

            <!-- Number Display -->
            <span class="fs-1 px-5 number">{{ number }}</span>

            <!-- Right Arrow Button -->
            <button class="btn btn-primary rounded-5" @click="incrementNumber">
              <font-awesome-icon :icon="['fas', 'angle-right']" />
            </button>
          </div>
          <p class="h-3 fw-bold fs-4 mb-1">Choose your goal!</p>
          <p class="h-4 fw-bold fs-6 text-primary">20 free offers left</p>
        </div>
      </div>

      <!-- Analytics Chart -->
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card p-3 shadow-sm bg-white">
          <h5 class="card-title">Analytics</h5>
          <!-- <GChart type="LineChart" :data="chartData" :options="chartOptions" /> -->
          <GoogleChart />
        </div>
      </div>
    </div>

    <div
      class="my-3 d-flex justify-content-center align-items-center p-5 bg-white rounded-3 border flex-column"
    >
      <button
        type="button"
        class="btn btn-primary btn-lg fs-3 fw-bold rounded-4"
        :disabled="store.count === false"
      >
        Search jobs
      </button>

      <div
        v-if="store.count === false"
        class="text-secondary mt-4 fs-5 w-50 text-center"
      >
        Please upload your resume in "About me" tab
      </div>
    </div>

    <div class="mt-4 bg-white p-3 rounded-3 border">
      <h4>Your Offers</h4>
      <table class="table">
        <thead>
          <tr>
            <th>Company</th>
            <th>Date</th>
            <th>Position</th>
            <th>Salary</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Apple</td>
            <td>12 Sep 2023</td>
            <td>Senior Developer</td>
            <td>$120,000</td>
            <td><span class="badge bg-success">Applied</span></td>
          </tr>
          <tr>
            <td>Amazon</td>
            <td>08 Aug 2023</td>
            <td>Project Manager</td>
            <td>$110,000</td>
            <td><span class="badge bg-warning">In Review</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { store } from "../../script/store.js";
</script>

<script>
// import { GChart } from "vue-google-charts";
import GoogleChart from "../GoogleChart";

export default {
  components: {
    // GChart,
    GoogleChart,
  },
  name: "Dashboard",
  methods: {
    incrementNumber() {
      if (this.number < 20) {
        this.number += 1; // Increase the number
      }
    },
    decrementNumber() {
      if (this.number > 0) {
        this.number -= 1; // Decrease the number
      }
    },
  },
  data: () => ({
    chartData: [
      ["Year", "A", "B", "C"],
      ["2014", 1000, 400, 200],
      ["2015", 1170, 460, 250],
      ["2016", 660, 1120, 300],
      ["2017", 1030, 540, 350],
    ],
    chartOptions: {
      chart: {
        title: "Statistics",
        subtitle: "A, B, C",
        lineWidth: 10,
        series: {
          0: { color: "#6f9654" },
          1: { color: "#1c91c0" },
          2: { color: "#43459d" },
        },
        // colors: ["green", "yellow", "gray"],
      },
    },
    number: 0,
  }),
};
</script>

<style scoped>
.card {
  height: 325px;
}

.counter {
  min-height: 165px;
  flex-wrap: wrap; /* Handles small screen sizes */
}
.number {
  font-size: clamp(
    2rem,
    9vw,
    70px
  ) !important; /* Scales number size based on viewport */
}
</style>
