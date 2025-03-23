<template>
  <div
    :class="[
      'd-flex border-end',
      'flex-column',
      'vh-100',
      { collapsed: isCollapsed },
    ]"
    id="sidebar"
  >
    <!-- Toggle Button -->
    <div class="text-center py-3 border-bottom" @click="toggleSidebar">
      <font-awesome-icon :icon="['fas', 'bars']" />
    </div>

    <!-- Sidebar Content -->
    <div class="flex-column p-3">
      <ul class="nav flex-column">
        <li class="nav-item py-1">
          <button
            class="btn btn-link text-start w-100 text-dark text-decoration-none"
            :class="{
              active: activeTab === 'dashboard',
              'border-start border-primary': activeTab === 'dashboard',
            }"
            @click="changeTab('dashboard')"
          >
            <font-awesome-icon :icon="['fas', 'briefcase']" />
            <span v-if="!isCollapsed" class="px-2">Dashboard</span>
          </button>
        </li>
        <li class="nav-item py-1">
          <button
            class="btn btn-link text-start w-100 text-dark text-decoration-none"
            :class="{
              active: activeTab === 'resume',
              'border-start border-primary': activeTab === 'resume',
            }"
            @click="changeTab('resume')"
          >
            <font-awesome-icon :icon="['fas', 'user']" />
            <span v-if="!isCollapsed" class="px-2">About me</span>
          </button>
        </li>
        <li class="nav-item py-1">
          <button
            class="btn btn-link text-start w-100 text-dark text-decoration-none"
            :class="{
              active: activeTab === 'applications',
              'border-start border-primary': activeTab === 'applications',
            }"
            @click="changeTab('applications')"
          >
            <font-awesome-icon :icon="['fas', 'file']" />
            <span v-if="!isCollapsed" class="px-2">Applications</span>
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "Sidebar",
  props: ["activeTab"],
  data() {
    return {
      isCollapsed: false, // Default state is expanded
    };
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed; // Toggle collapse state
    },
    changeTab(tab) {
      this.$emit("update:activeTab", tab); // Emit event to change active tab
    },
  },
};
</script>

<style scoped>
#sidebar .nav-item button {
  display: flex;
  align-items: center;
  border: none; /* Remove any default border */
  outline: none; /* Remove focus outline */
  padding: 0.5rem; /* Ensure padding for spacing */
}

#sidebar .nav-item button.border-start {
  border-left-width: 3px !important; /* Add custom left border */
}

#sidebar .nav-item button.border-primary {
  border-color: #0d6efd !important; /* Use Bootstrap's primary color */
  border-radius: 0;
}

button.active {
  font-weight: bold;
}

button.border-start {
  border-left-width: 4px !important; /* Make the border prominent */
}

button.border-primary {
  border-color: #0d6efd !important; /* Use Bootstrap's primary color */
}

#sidebar .nav-item button span {
  transition: opacity 0.3s ease;
}

#sidebar.collapsed .nav-item button span {
  opacity: 0;
}
</style>
