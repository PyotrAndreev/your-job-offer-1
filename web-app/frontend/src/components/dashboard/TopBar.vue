<template>
  <nav class="navbar navbar-light border-bottom bg-white shadow-sm">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <!-- Styled like a button -->
      <a
        href="./"
        class="btn d-flex align-items-center gap-2 "
      >
        <font-awesome-icon :icon="['fas', 'house']" style="color: #0d6efd"/>
        <span class="d-none d-sm-inline">Your job offer</span>
      </a>

      <!-- Styled Dropdown -->
      <div class="dropdown nav-item me-3">
        <button
          class="btn dropdown-toggle rounded-pill border"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          {{ userName }}
        </button>
        <ul
          class="dropdown-menu dropdown-menu-end shadow rounded"
          aria-labelledby="dropdownMenuButton1"
        >
          <li>
            <a class="dropdown-item" href="/">
              <i class="fas fa-arrow-left me-2"></i>Возврат на главную
            </a>
          </li>
          <li>
            <a class="dropdown-item" href="/#features">
              <i class="fas fa-star me-2"></i>Наши фишки
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      userName: "Ваш аккаунт",
    };
  },
  mounted() {
    const savedData = localStorage.getItem("formData");
    if (savedData) {
      this.userName = JSON.parse(savedData).firstName;
    }
  },
};
</script>

<style scoped>
.navbar {
  height: 60px;
}

.btn {
  transition: background-color 0.2s ease-in-out, box-shadow 0.2s;
}

.btn:hover {
  background-color: #f8f9fa;
}

.dropdown-menu a.dropdown-item:hover {
  background-color: #f8f9fa;
}
</style>
