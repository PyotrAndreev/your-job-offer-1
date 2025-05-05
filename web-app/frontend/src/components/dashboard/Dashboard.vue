 <template>
  <div class="p-3 p-md-4 bg-light min-vh-100">
    <h2 class="mb-4">Дэшборд</h2>

    <div class="bg-white rounded-4 border p-3 p-md-4 mb-4 shadow-sm">
      <!-- Mode Toggle Section -->
      <div class="d-flex flex-column align-items-center mb-3 mb-md-4 gap-2 gap-md-3">
        <div class="d-flex align-items-center gap-2 gap-md-3 flex-wrap justify-content-center position-relative">
          <span class="fw-semibold">Режим подбора</span>

          <!-- Toggle Switch -->
          <div class="form-check form-switch ms-1">
            <input
              class="form-check-input"
              style="width: 50px"
              type="checkbox"
              role="switch"
              id="modeSwitch"
              v-model="isAutoMode"
            >
            <label class="form-check-label ms-2 ms-md-3 mt-1" for="modeSwitch">
              {{ isAutoMode ? 'Авто' : 'Ручной' }}
            </label>
          </div>

          <!-- Tooltip -->
          <font-awesome-icon
            icon="question-circle"
            class="text-muted ms-1 ms-md-2"
            @mouseenter="showTooltip = true"
            @mouseleave="showTooltip = false"
          />
          <div v-if="showTooltip" class="tooltip-custom">
            <p>В ручном режиме вы выбираете понравившиеся вакансии, а мы подаемся на них за вас.
            В авто — система будет подаваться на вакансии, пока не получится найти указанное количество предложений.</p>
          </div>
        </div>
      </div>

      <!-- Count and Button -->
      <div class="text-center mb-4 mb-md-5">
        <h5 class="mb-2 mb-md-3 h4 h-md-3">Сколько предложений хотите найти?</h5>
        <div class="d-flex align-items-center justify-content-center counter mb-2 mb-md-3 flex-wrap">
          <button
            class="btn btn-outline-primary rounded-circle px-2 px-md-3 py-1 py-md-2"
            @click="decrementNumber"
            :disabled="store.userFilledData === false"
          >
            <font-awesome-icon :icon="['fas', 'angle-left']" />
          </button>

          <span class="fs-2 fs-md-1 px-3 px-md-5 number">{{ number }}</span>

          <button
            class="btn btn-outline-primary rounded-circle px-2 px-md-3 py-1 py-md-2"
            @click="incrementNumber"
            :disabled="store.userFilledData === false"
          >
            <font-awesome-icon :icon="['fas', 'angle-right']" />
          </button>
        </div>

        <button
          type="button"
          class="btn btn-primary btn-md btn-lg fw-bold px-4 px-md-5 py-1 py-md-2"
          :disabled="store.userFilledData === false"
          @click="searchOffers"
        >
          Найти вакансии
        </button>

        <div 
          v-if="store.userFilledData === false" 
          class="modern-alert alert-info"
        >
          <div class="alert-content">
            <!-- <font-awesome-icon :icon="['fas', 'circle-info']" class="alert-icon"/> -->
            <!-- <div> -->
              <h6 class="alert-title">Требуется действие</h6>
              <p class="alert-message">Пожалуйста, заполните анкету во вкладке "Профиль"</p>
            <!-- </div> -->
          </div>
        </div>

        <div 
          v-if="store.userAuthorizedWithHH === false" 
          class="modern-alert alert-warning"
        >
          <div class="alert-content">
            <h6 class="alert-title">Требуется авторизация</h6>
            <p class="alert-message">
              Нам нужно разрешение подаваться на вакансии hh.ru от вашего лица.
              <a 
                href="https://hh.ru/oauth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI" 
                class="alert-link"
                @click.prevent="handleAuthRedirect"
              >
                Предоставить доступ
              </a>
            </p>
          </div>
        </div>


      </div>

      <!-- Auto Mode Table -->
      <div v-if="isAutoMode && offers.length" class="mt-4 mt-md-5">
        <h5 class="text-center">Найдено {{ offers.length }} из {{ number }} вакансий</h5>
        <div class="table-responsive mt-3 mt-md-4">
          <table class="table table-bordered table-hover align-middle shadow-sm">
            <thead class="table">
              <tr>
                <th>Компания</th>
                <th>Дата</th>
                <th>Позиция</th>
                <th>Зарплата</th>
                <th>Сайт</th>
                <th>Статус</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="offer in offers" :key="offer.link">
                <td>{{ offer.company }}</td>
                <td>{{ offer.date }}</td>
                <td>{{ offer.position }}</td>
                <td>{{ offer.salary }}</td>
                <td><a :href="offer.link" target="_blank" class="text-nowrap">сайт</a></td>
                <td><span class="badge bg-success">Отклик подан</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Manual Mode Cards -->
      <div v-if="!isAutoMode && offers.length" class="mt-4 mt-md-5">
        <h5 class="text-center mb-3 mb-md-4">Выберите понравившиеся вакансии</h5>
        <div class="row row-cols-1 row-cols-sm-2 row-cols-lg-3 g-3">
          <div
            class="col"
            v-for="(offer, index) in offers"
            :key="offer.link"
            @click="toggleSelection(index)"
          >
            <div
              class="card offer-card shadow-sm h-100"
              :class="{ 'selected-card': offer.selected }"
            >
              <div class="card-body d-flex flex-column p-3">
                <h5 class="card-title mb-1 mb-md-2">{{ offer.position }}</h5>
                <h6 class="card-subtitle mb-1 mb-md-2 text-muted">{{ offer.company }}</h6>
                
                <div class="mt-auto">
                  <p class="card-text mb-1 mb-md-2 h1">Зарплата: <small class="text-muted">{{ offer.salary }}</small></p>
                  <p class="card-text mb-1 mb-md-2">Дата: <small class="text-muted">{{ offer.date }}</small></p>
                  <a 
                    :href="offer.link" 
                    class="btn btn-outline-primary w-100 mt-2"
                    target="_blank"
                    @click.stop
                  >
                    Подробнее
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="text-end mt-3 mt-md-4 d-flex justify-content-center">
          <button class="btn btn-primary px-4 py-2" @click="submitSelected">Отправить отклики</button>
        </div>
      </div>
    </div>

    <!-- Analytics Section -->
    <div class="row g-3 g-md-4 justify-content-center">
      <div class="col-12 col-md-6">
        <div class="card p-3 p-md-4 text-center shadow-sm h-100">
          <h5 class="card-title mb-2 mb-md-3">Прогресс</h5>
          <div class="text-muted">
            <font-awesome-icon :icon="['fas', 'chart-line']" size="2x" size-md="3x" class="mb-1 mb-md-2" />
            <p class="mb-0">График прогресса появится здесь.</p>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6">
        <div class="card p-3 p-md-4 text-center shadow-sm h-100">
          <h5 class="card-title mb-2 mb-md-3">Аналитика</h5>
          <div class="text-muted">
            <font-awesome-icon :icon="['fas', 'chart-pie']" size="2x" size-md="3x" class="mb-1 mb-md-2" />
            <p class="mb-0">Общая статистика будет доступна здесь.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { store } from "../../script/store.js";

const number = ref(3);
const isAutoMode = ref(false);
const showTooltip = ref(false);

const offers = ref([
  {
    company: "amoCRM",
    date: "15 Dec 2024",
    position: "Frontend Developer",
    salary: "до 50 000 ₽",
    link: "https://hh.ru/vacancy/111898417",
    selected: false
  },
  {
    company: "Yandex",
    date: "20 Dec 2024",
    position: "Junior React Dev",
    salary: "до 60 000 ₽",
    link: "https://hh.ru/vacancy/123456789",
    selected: false
  },
  {
    company: "VK",
    date: "22 Dec 2024",
    position: "Vue.js Developer",
    salary: "до 70 000 ₽",
    link: "https://hh.ru/vacancy/987654321",
    selected: false
  },
  {
    company: "SberTech",
    date: "25 Dec 2024",
    position: "Angular Developer",
    salary: "до 80 000 ₽",
    link: "https://hh.ru/vacancy/456789123",
    selected: false
  },
  {
    company: "Tinkoff",
    date: "28 Dec 2024",
    position: "Fullstack Developer",
    salary: "до 90 000 ₽",
    link: "https://hh.ru/vacancy/321654987",
    selected: false
  },
  {
    company: "Ozon",
    date: "30 Dec 2024",
    position: "Node.js Developer",
    salary: "до 100 000 ₽",
    link: "https://hh.ru/vacancy/654987321",
    selected: false
  }
]);

function incrementNumber() {
  if (number.value < 20) number.value++;
}
function decrementNumber() {
  if (number.value > 1) number.value--;
}
function searchOffers() {
  offers.value = offers.value.map(o => ({ ...o, selected: false }));
}
function toggleSelection(index) {
  offers.value[index].selected = !offers.value[index].selected;
}
function submitSelected() {
  const selected = offers.value.filter(o => o.selected);
  alert(`Вы откликнулись на ${selected.length} вакансии.`);
}
function handleAuthRedirect() {
  const clientId = process.env.HH_CLIENT_ID; // Замените на ваш client_id
  const redirectUri = process.env.HH_REDIRECT_URL; // Ваш URL для callback

  window.location.href = `https://hh.ru/oauth/authorize?response_type=code&client_id=${clientId}&redirect_uri=${redirectUri}`;
}
</script>

<style scoped>
.form-switch .form-check-input {
  width: 2.5em;
  height: 1.4em;
  cursor: pointer;
}

.form-switch .form-check-input:focus {
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-check-label {
  cursor: pointer;
  user-select: none;
}

.counter {
  min-height: 80px;
}

.number {
  font-size: clamp(1.5rem, 8vw, 3.5rem) !important;
}

.tooltip-custom {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 10;
  background-color: #575757;
  color: #ffffff;
  padding: 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  white-space: normal;
  opacity: 0.95;
  width: 280px;
  max-width: 90vw;
}

/* Card styles */
.offer-card {
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 0.75rem;
  overflow: hidden;
  position: relative;
  border: 1px solid #e9ecef;
  min-height: 220px;
}

.offer-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.selected-card {
  border: 2px solid #0d6efd;
  background-color: #f8faff;
}

.selected-card::after {
  content: '✓';
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 1.5rem;
  height: 1.5rem;
  background-color: #0d6efd;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
}

.card-title {
  font-size: 1.2rem !important;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.3;
}

.card-subtitle {
  font-size: 0.85rem;
  margin-bottom: 0.75rem;
  color: #6c757d;
}

.card-text {
  font-size: 1rem !important;
  margin-bottom: 0.25rem;
  line-height: 1.4;
}

.card-text small {
  color: #6c757d;
}

.btn-outline-primary {
  border-radius: 0.5rem;
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

/* Responsive adjustments */
@media (min-width: 768px) {
  .offer-card {
    min-height: 260px;
  }
  
  .card-title {
    font-size: 1.1rem;
  }
  
  .card-subtitle {
    font-size: 0.9rem;
  }
  
  .card-text {
    font-size: 0.85rem;
  }
  
  .btn-outline-primary {
    padding: 0.375rem 0.75rem;
    font-size: 0.85rem;
  }
}

@media (min-width: 992px) {
  .offer-card {
    min-height: 280px;
  }
}

.modern-alert {
  max-width: 450px;
  margin: 1.5rem auto;
  padding: 1rem 1.25rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: none;
  transition: all 0.3s ease;
  animation: fadeIn 0.5s ease-out;
}

.alert-info {
  background-color: #f0f7ff;
  color: #0066cc;
}

.alert-warning {
  background-color: #fff8e6;
  color: #e67e00;
}

.alert-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.alert-icon {
  font-size: 1.25rem;
  margin-top: 2px;
  flex-shrink: 0;
}

.alert-title {
  font-weight: 600;
  font-size: 0.95rem;
}

.alert-message {
  margin: 0;
  font-size: 0.90rem;
  line-height: 1.4;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Ховер-эффекты */
.modern-alert:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.alert-link {
  color: inherit;
  text-decoration: underline;
  font-weight: 600;
  transition: color 0.2s;
}

.alert-link:hover {
  color: #0056b3;
  text-decoration: none;
}
</style>