<template>
  <nav class="navbar navbar-light border-bottom">
    <div class="container-fluid">
      <form class="d-flex">
        <input
          class="form-control me-2 mx-2"
          type="search"
          placeholder="Search applications"
          aria-label="Search"
        />
        <button class="btn border-0" type="submit">
          <font-awesome-icon
            :icon="['fas', 'magnifying-glass']"
            style="color: #212529"
          />
        </button>
      </form>
      <div class="dropdown nav-item mx-5">
        <button
          class="btn dropdown-toggle border-0"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          Username
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1">
          <li><a class="dropdown-item" href="#home">Return to main</a></li>
          <li>
            <a class="dropdown-item" href="#home#features">See our fetures</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
button:hover {
  background-color: #e9ecef;
}
</style>
