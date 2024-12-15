<template>
  <div class="d-flex">
    <!-- Sidebar -->
    <Sidebar :activeTab="activeTab" @update:activeTab="updateTab" />

    <!-- Main Content -->
    <div class="flex-grow-1">
      <TopBar />

      <div v-if="activeTab === 'resume'">
        <EditResume />
      </div>
      <div v-if="activeTab === 'dashboard'">
        <Dashboard />
      </div>
      <div v-if="activeTab === 'applications'">
        <Applications />
      </div>
    </div>
  </div>
</template>

<script setup>
import { store } from "../../script/store.js";
</script>

<script>
import Sidebar from "./Sidebar.vue";
import EditResume from "./EditResume.vue";
import Dashboard from "./Dashboard.vue";
import Applications from "./Applications.vue";
import TopBar from "./TopBar.vue";

export default {
  name: "App",
  components: {
    Sidebar,
    EditResume,
    Dashboard,
    Applications,
    TopBar,
  },
  data() {
    return {
      activeTab: "dashboard",
    };
  },
  methods: {
    updateTab(tab) {
      this.activeTab = tab;
    },
  },
};
</script>

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>
