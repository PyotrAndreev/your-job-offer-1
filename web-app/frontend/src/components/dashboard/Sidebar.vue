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
    <div class="text-center border-bottom toggle" @click="toggleSidebar">
      <font-awesome-icon :icon="['fas', 'bars']" />
    </div>

    <!-- Sidebar Content -->
    <div class="flex-column p-3">
      <ul class="nav flex-column">
        <li class="nav-item py-1">
          <button
            class="btn btn-link text-start w-100 text-dark text-decoration-none"
            @click="changeTab('dashboard')"
            :class="{
              active: activeTab === 'dashboard',
            }"
          >
            <font-awesome-icon :icon="['fas', 'briefcase']" 
            :class="{
              'color': activeTab === 'dashboard',
            }"/>
            <span v-if="!isCollapsed" class="px-2">Дэшборд</span>
          </button>
        </li>
        <li class="nav-item py-1">
          <button
            class="btn btn-link text-start w-100 text-dark text-decoration-none"
            :class="{
              active: activeTab === 'resume',
              '': activeTab === 'resume',
            }"
            @click="changeTab('resume')"
          >
            <font-awesome-icon :icon="['fas', 'user']" 
            :class="{
              'color': activeTab === 'resume',
            }"/>
            <span v-if="!isCollapsed" class="px-2">Профиль</span>
          </button>
        </li>
        <li class="nav-item py-1">
          <button
            class="btn btn-link text-start w-100 text-dark text-decoration-none"
            :class="{
              active: activeTab === 'applications',
              '': activeTab === 'applications',
            }"
            @click="changeTab('applications')"
          >
            <font-awesome-icon :icon="['fas', 'file']" 
            :class="{
              'color': activeTab === 'applications',
            }"/>
            <span v-if="!isCollapsed" class="px-2">История</span>
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
      isCollapsed: true, // Default state is expanded
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

/* #sidebar .nav-item button.border-start {
  border-left-width: 3px !important; 
}

#sidebar .nav-item button.border-primary {
  border-color: #0d6efd !important;
  border-radius: 0;
} */

button.active {
  background-color: #f8f9fa;
    /* font-weight: bold; */
}

/* button.border-start {
  border-left-width: 4px !important; 
} */

/* button.border-primary {
  border-color: #0d6efd !important; 
} */

#sidebar .nav-item button span {
  transition: opacity 0.3s ease;
}

#sidebar.collapsed .nav-item button span {
  opacity: 0;
}

.toggle {
  height: 60px;
  padding: 20px;  
}

.color {
  color: #0d6efd;
}

</style>
