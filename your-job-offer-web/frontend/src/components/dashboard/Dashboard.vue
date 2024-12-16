<template>
  <div class="p-4 bg-light">
    <h2 class="mb-4">Dashboard</h2>
    <div class="row g-4">
      <!-- Progress Card -->
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card p-3 text-center shadow-sm">
          <h5 class="card-title">Progress</h5>
          <!-- <GChart type="AreaChart" :data="chartData" :options="chartOptions" /> -->
          <PieChart />
        </div>
      </div>

      <!-- Offers Goal -->
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card p-3 text-center shadow-sm">
          <h5 class="card-title">How many offers to find?</h5>
          <div
            class="d-flex align-items-center justify-content-center counter w-100"
          >
            <!-- Left Arrow Button -->
            <button
              class="btn btn-primary rounded-5"
              @click="decrementNumber"
              :disabled="store.userFilledData === false"
            >
              <font-awesome-icon :icon="['fas', 'angle-left']" />
            </button>

            <!-- Number Display -->
            <span class="fs-1 px-5 number">{{ number }}</span>

            <!-- Right Arrow Button -->
            <button
              class="btn btn-primary rounded-5"
              @click="incrementNumber"
              :disabled="store.userFilledData === false"
            >
              <font-awesome-icon :icon="['fas', 'angle-right']" />
            </button>
          </div>
          <p class="h-3 fw-bold fs-4 mb-1">Choose your goal!</p>
          <p class="h-4 fw-bold fs-6 text-primary">20 free offers left</p>
        </div>
      </div>

      <!-- Analytics Chart -->
      <div class="col-12 col-md-6 col-lg-4">
        <div class="card p-3 shadow-sm text-center bg-white">
          <h5 class="card-title">Analytics</h5>
          <!-- <GChart type="LineChart" :data="chartData" :options="chartOptions" /> -->
          <AreaChart />
        </div>
      </div>
    </div>

    <div
      class="my-3 d-flex justify-content-center align-items-center p-5 bg-white rounded-3 border flex-column"
    >
      <button
        type="button"
        class="btn btn-primary btn-lg fs-3 fw-bold rounded-4"
        :disabled="store.userFilledData === false"
        @click="searchOffers"
      >
        Search jobs
      </button>

      <div
        v-if="store.userFilledData === false"
        class="text-secondary mt-4 fs-5 w-50 text-center"
      >
        Please fill in your data in "About me" tab
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
          <tr v-for="offer in offers">
            <td>{{ offer.company }}</td>
            <td>{{ offer.date }}</td>
            <td>{{ offer.position }}</td>
            <td>{{ offer.salary }}</td>
            <td>
              <a :href="offer.link" target="_blank">сайт работодателя</a>
            </td>
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
import AreaChart from "./AreaChart.js";
import PieChart from "./PieChart.js";

export default {
  components: {
    AreaChart,
    PieChart,
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
    async searchOffers() {
      this.newOffer = {
        company: "amoCrm",
        date: "15 Dec 2024",
        position: "Junior frontend developer",
        salary: "до 50 000 ₽",
        status: "awaiting",
        link: "https://hh.ru/vacancy/111898417?hhtmFromLabel=suitable_vacancies&hhtmFrom=vacancy",
      };

      setTimeout(() => {
        this.offers.push({ ...this.newOffer });
      }, 5000);
    },
  },
  data: () => ({
    number: 0,

    offers: [],
    newOffer: {
      company: "",
      date: "",
      position: "",
      salary: "",
      status: "",
      link: "",
    },
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
