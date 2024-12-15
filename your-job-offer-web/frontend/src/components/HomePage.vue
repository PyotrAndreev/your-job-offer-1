<template>
  <!-- Navigation Bar -->
  <nav class="navbar navbar-expand-lg navbar-light border-bottom border-2">
    <div class="container">
      <a class="navbar-brand fs-4 fw-normal" href="#home">
        <img src="../assets/logo.svg" />
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <button
              class="nav-link"
              v-on:click="scrollToSection('testimonials')"
            >
              Отзывы
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link" v-on:click="scrollToSection('pricing')">
              Тарифы
            </button>
          </li>
          <li class="nav-item">
            <button
              class="nav-link me-3"
              v-on:click="scrollToSection('contact')"
            >
              Контакты
            </button>
          </li>
          <li class="nav-item">
            <div class="d-grid gap-2 d-md-flex">
              <a class="btn btn-outline-primary" href="#login">Войти</a>
              <a class="btn btn-primary" href="#registration">Регистрация</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <div class="hero text-center">
    <div class="container p-4">
      <h1 class="display-3 fw-bold lh-1">Самый быстрый оффер</h1>
      <h1 class="display-3 fw-bold lh-1">в твоей карьере</h1>
      <p class="lead fs-4 my-3">
        Сервис для автоматического поиска вакансий и стажировок
      </p>
      <a href="#registration" class="btn btn-primary btn-lg">Начать сейчас</a>
    </div>
  </div>

  <!-- Features Section -->
  <div
    id="preview"
    class="preview text-center border-bottom border-top border-2"
  >
    <div class="container py-4">
      <h2 class="mb-4">Как все устроенно?</h2>
      <div class="row">
        <div class="col-md-4">
          <div class="card border" style="height: 500px">
            <div class="card-body">
              <h5 class="card-title fw-bold">
                Шаг
                <font-awesome-icon
                  :icon="['fas', '1']"
                  style="color: #3b65e3"
                />
              </h5>
              <p class="card-text">
                Заполните анкету для создания резюме или прикрепите свое
              </p>
              <div
                class="preview-image mx-auto mb-2 border rounded-3 d-flex justify-content-center align-items-center"
              >
                <span class="fw-bold fs-3 border p-3 rounded-5 shadow"
                  >Service prview</span
                >
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border" style="height: 500px">
            <div class="card-body">
              <h5 class="card-title fw-bold">
                Шаг
                <font-awesome-icon
                  :icon="['fas', '2']"
                  style="color: #3b65e3"
                />
              </h5>
              <p class="card-text">
                Выберите количество карьерных предложений, которые хотите
                получить
              </p>
              <div
                class="preview-image mx-auto mb-2 border rounded-3 d-flex justify-content-center align-items-center"
              >
                <span class="fw-bold fs-3 border p-3 rounded-5 shadow"
                  >Service prview</span
                >
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border">
            <div class="card-body">
              <h5 class="card-title fw-bold">
                Шаг
                <font-awesome-icon
                  :icon="['fas', '3']"
                  style="color: #3b65e3"
                />
              </h5>
              <p class="card-text">
                Сервис автоматически выберет лучшие возможности для развития
                вашей карьеры
              </p>
              <div
                class="preview-image mx-auto mb-2 border rounded-3 d-flex justify-content-center align-items-center"
              >
                <span class="fw-bold fs-3 border p-3 rounded-5 shadow"
                  >Service prview</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Testimonials Section -->
  <div id="testimonials" class="testimonial text-center">
    <div class="container py-4">
      <h2 class="mb-4 pb-4">Отзывы пользователей</h2>
      <div class="row gx-4 justify-content-evenly">
        <div class="col-md-5 border rounded-pill border-secondary border-2">
          <blockquote class="blockquote">
            <p class="my-3 mx-auto" style="max-width: 350px">
              "Отличный сервис! Помог мне быстро найти стажировку"
            </p>
            <footer class="blockquote-footer pt-1">
              Довольный клиент, <cite title="Source Title">Студент</cite>
            </footer>
          </blockquote>
        </div>
        <div class="col-md-5 border rounded-pill border-secondary border-2">
          <blockquote class="blockquote">
            <p class="my-3 mx-auto" style="max-width: 350px">
              "Нашел вакансию мечты благодаря сервису, однозначно рекомендую!"
            </p>
            <footer class="blockquote-footer pt-1">
              Еще один клиент,
              <cite title="Source Title">Айти специалист</cite>
            </footer>
          </blockquote>
        </div>
      </div>
    </div>
  </div>

  <!-- Pricing Section -->
  <div
    id="pricing"
    class="pricing text-center mb-5 py-5 border-top border-bottom border-2"
  >
    <div class="container mb-4 py-4">
      <h2 class="mb-5">Тарифы</h2>
      <div class="row">
        <div class="col-md-4">
          <div class="card border-primary">
            <div class="card-body px-5 mx-3 pb-5">
              <h5 class="card-title fw-bold">Базовый</h5>
              <p class="card-text mb-1 text-start">
                - Поиск до 20 вакансий в месяц
              </p>
              <p class="card-text mb-1 text-start">
                - Дополнительные ограничения
              </p>
              <p class="card-text mb-1 text-start">
                - И еще несколько ограничений
              </p>
              <p class="card-text mb-1 text-start">
                - И еще несколько ограничений
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div
            class="card text-light rounded-3"
            style="background-color: #3d8bfd"
          >
            <div class="card-body px-5 mx-3 pb-5">
              <h5 class="card-title fw-bold">Основной</h5>
              <p class="card-text mb-1 text-start">
                - Без ограничений на число вакансий
              </p>
              <p class="card-text mb-1 text-start">
                - Дополнительные преимущества
              </p>
              <p class="card-text mb-1 text-start">
                - Еще несколько преимуществ
              </p>
              <p class="card-text mb-1 text-start">
                - Еще несколько преимуществ
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border-primary">
            <div class="card-body px-5 mx-3 pb-5">
              <h5 class="card-title fw-bold">Премиум</h5>
              <p class="card-text mb-1 text-start">
                - Полный доступ ко всем функциям
              </p>
              <p class="card-text mb-1 text-start">- Продвинутая аналитика</p>
              <p class="card-text mb-1 text-start">
                - Дополнительные преимущества
              </p>
              <p class="card-text mb-1 text-start">
                - Еще несколько преимуществ
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Contact Section -->
  <div id="contact" class="text-center pb-2">
    <div class="container my-5 py-5">
      <h2 class="mb-2">Свяжитесь с нами!</h2>
      <p>Обращайтесь по любым вопросам, наши специалисты всегда на связи</p>
      <a href="mailto:info@myservice.com" class="btn btn-primary">
        Написать на почту
      </a>
    </div>
  </div>

  <!-- Footer Section -->
  <footer class="footer text-center">
    <div class="container">
      <p>&copy; 2024 Your-job-offer. All rights reserved.</p>
    </div>
  </footer>
</template>

<script>
export default {
  methods: {
    scrollToSection(id) {
      const section = document.getElementById(id);
      if (section) {
        section.scrollIntoView({ behavior: "smooth" });
      }
    },
  },
};
</script>

<style scoped>
.hero {
  padding: 60px 0;
}
.preview {
  padding: 40px 0;
}
.preview-image {
  height: 350px;
  width: 80%;
  transition: all 0.3s ease-in-out;
  color: #495057;
}

.preview-image:hover {
  border: 1px solid #0d6efd !important;
}
.testimonial {
  padding: 40px 0;
  margin-bottom: 50px;
}
.footer {
  background-color: #343a40;
  color: white;
  padding: 20px 0;
}
</style>
