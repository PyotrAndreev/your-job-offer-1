<template>
  <!-- Navigation Bar -->
  <nav class="navbar navbar-expand-lg navbar-light border-bottom border-2 bg-white">
    <div class="container">
      <a class="navbar-brand fs-4 fw-normal" href="home">
        <img src="../assets/logotype.svg" alt="Логотип" class="logo-hover">
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
              class="nav-link nav-link-custom"
              v-on:click="scrollToSection('testimonials')"
            >
              Отзывы
            </button>
          </li>
          <li class="nav-item">
            <button class="nav-link nav-link-custom" v-on:click="scrollToSection('pricing')">
              Тарифы
            </button>
          </li>
          <li class="nav-item">
            <button
              class="nav-link nav-link-custom me-3"
              v-on:click="scrollToSection('contact')"
            >
              Контакты
            </button>
          </li>
          <li class="nav-item">
            <div class="d-grid gap-2 d-md-flex">
              <a class="btn btn-outline-primary btn-hover" href="login">Войти</a>
              <a class="btn btn-primary btn-hover" href="registration">Регистрация</a>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <div class="hero text-center">
    <div class="container p-4 hero-content">
      <h1 class="display-3 fw-bold lh-1 animate__animated animate__fadeInDown">Самый быстрый оффер</h1>
      <h1 class="display-3 fw-bold lh-1 animate__animated animate__fadeInDown animate__delay-1s">в твоей карьере</h1>
      <p class="lead fs-4 my-3 animate__animated animate__fadeIn animate__delay-2s">
        Сервис для автоматического поиска вакансий и стажировок
      </p>
      <a href="registration" class="btn btn-primary btn-lg mt-3 btn-pulse">Начать сейчас</a>
    </div>
  </div>

  <!-- Features Section -->
  <div
    id="preview"
    class="preview text-center border-bottom border-top border-2"
  >
    <div class="container py-4">
      <h2 class="mb-4 animate__animated animate__fadeIn">Как все устроенно?</h2>
      <div class="row">
        <div class="col-md-4">
          <div class="card border bg-light preview-card" style="height: 500px">
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
              <img 
                src="../assets/1.svg" 
                style="width: 100%; height: 350px"
                class="rounded-3 mx-auto mb-2 img-float"
              />
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border bg-light preview-card" style="height: 500px">
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
              <img 
                src="../assets/2.svg" 
                style="width: 90%; height: 350px"
                class="rounded-3 mx-auto mb-2 img-float"
              />
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card border bg-light preview-card" style="height: 500px">
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
              <img 
                src="../assets/3.svg" 
                style="width: 100%; height: 350px"
                class="rounded-3 mx-auto mb-2 img-float"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Testimonials Section -->
  <div id="testimonials" class="testimonial text-center">
    <div class="container py-4">
      <h2 class="mb-4 pb-4 animate__animated animate__fadeIn">Отзывы пользователей</h2>
      <div class="row gx-4 justify-content-evenly">
        <div class="col-md-5 border rounded-pill border-secondary border-2 testimonial-card">
          <blockquote class="blockquote">
            <p class="my-3 mx-auto" style="max-width: 350px">
              "Отличный сервис! Помог мне быстро найти стажировку"
            </p>
            <footer class="blockquote-footer pt-1">
              Довольный клиент, <cite title="Source Title">Студент</cite>
            </footer>
          </blockquote>
        </div>
        <div class="col-md-5 border rounded-pill border-secondary border-2 testimonial-card">
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
      <h2 class="mb-5 animate__animated animate__fadeIn">Тарифы</h2>
      <div class="row">
        <div class="col-md-4">
          <div class="card border-primary pricing-card">
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
            class="card text-light rounded-3 pricing-card-main"
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
          <div class="card border-primary pricing-card">
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
      <h2 class="mb-2 animate__animated animate__fadeIn">Свяжитесь с нами!</h2>
      <p class="animate__animated animate__fadeIn animate__delay-1s">Обращайтесь по любым вопросам, наши специалисты всегда на связи</p>
      <a href="mailto:info@myservice.com" class="btn btn-primary btn-hover animate__animated animate__fadeIn animate__delay-2s">
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
  mounted() {
    // Анимация при скролле
    const animateOnScroll = () => {
      const elements = document.querySelectorAll('.animate__animated');
      
      elements.forEach(element => {
        const elementPosition = element.getBoundingClientRect().top;
        const screenPosition = window.innerHeight / 1.3;
        
        if (elementPosition < screenPosition) {
          const animation = element.getAttribute('data-animation');
          element.classList.add(animation);
        }
      });
    };
    
    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Инициализация при загрузке
  }
};
</script>

<style scoped>

.hero {
  padding: 60px 0 60px;
}
.preview {
  padding: 40px 0;
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

.logo-hover {
  transition: transform 0.3s ease;
}
.logo-hover:hover {
  transform: scale(1.05);
}

.nav-link-custom {
  transition: all 0.3s ease;
  position: relative;
  padding: 5px 0;
  border: none;
  background: none;
}
.nav-link-custom:hover {
  color: #0d6efd !important;
}
.nav-link-custom::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #0d6efd;
  transition: width 0.3s ease;
}
.nav-link-custom:hover::after {
  width: 100%;
}

.btn-hover {
  transition: all 0.3s ease;
  transform: translateY(0);
}
.btn-hover:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.btn-pulse {
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(13, 110, 253, 0.4);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(13, 110, 253, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(13, 110, 253, 0);
  }
}

.preview-card {
  transition: all 0.4s ease;
}
.preview-card:hover {
  border-color: #0d6efd !important;
  transform: translateY(-10px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.img-float {
  transition: transform 0.5s ease;
}
.preview-card:hover .img-float {
  transform: scale(1.05);
}

.testimonial-card {
  transition: all 0.3s ease;
}
.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.pricing-card, .pricing-card-main {
  transition: all 0.4s ease;
  height: 100%;
}
.pricing-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}
.pricing-card-main:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 25px rgba(61, 139, 253, 0.3);
}

.hero-content {
  opacity: 0;
  animation: fadeIn 1s ease forwards 0.5s;
}
@keyframes fadeIn {
  to {
    opacity: 1;
  }
}
</style>