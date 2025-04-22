<!-- <template>
  <div class="p-4 bg-light min-vh-100">
    <h2 class="mb-4">Dashboard</h2>

    <div class="bg-white rounded-3 border p-4 p-md-5 mb-5 d-flex flex-column align-items-center shadow-sm">

      <div class="text-center mb-3 w-100">
        <h5 class="mb-3 h3">How many offers you want to get?</h5>
        <div class="d-flex align-items-center justify-content-center counter mb-3 flex-wrap">
          <button
            class="btn btn-outline-primary rounded-circle px-3 py-2"
            @click="decrementNumber"
            :disabled="store.userFilledData === false"
          >
            <font-awesome-icon :icon="['fas', 'angle-left']"/>
          </button>

          <span class="fs-1 px-5 number">{{ number }}</span>

          <button
            class="btn btn-outline-primary rounded-circle px-3 py-2"
            @click="incrementNumber"
            :disabled="store.userFilledData === false"
          >
            <font-awesome-icon :icon="['fas', 'angle-right']"/>
          </button>
        </div>
        <p class="fw-bold fs-5 mb-3">Choose your goal!</p>
      </div>

      <div class="d-flex justify-content-center w-100 mb-2">
        <button
          type="button"
          class="btn btn-primary btn-lg fw-bold px-5 py-2"
          :disabled="store.userFilledData === false"
          @click="searchOffers"
        >
          Search jobs
        </button>
      </div>

      <div
        v-if="store.userFilledData === false"
        class="text-secondary mt-4 fs-6 text-center"
      >
        Please fill in your data in the "About me" tab
      </div>
    </div>

    <div class="row g-4 justify-content-center">
      <div class="col-12 col-md-6">
        <div class="card p-4 text-center shadow-sm h-100">
          <h5 class="card-title mb-3">Progress</h5>
          <div class="text-muted">
            <font-awesome-icon :icon="['fas', 'chart-line']" size="3x" class="mb-2" />
            <p>Progress chart will appear here soon.</p>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6">
        <div class="card p-4 text-center shadow-sm h-100">
          <h5 class="card-title mb-3">Analytics</h5>
          <div class="text-muted">
            <font-awesome-icon :icon="['fas', 'chart-pie']" size="3x" class="mb-2" />
            <p>Analytics summary will be displayed here.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="mt-5 bg-white p-3 rounded-3 border shadow-sm">
      <h4 class="mb-3">Your Offers</h4>
      <div class="table-responsive">
        <table class="table align-middle">
          <thead class="table-light">
            <tr>
              <th>Company</th>
              <th>Date</th>
              <th>Position</th>
              <th>Salary</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="offer in offers" :key="offer.link">
              <td>{{ offer.company }}</td>
              <td>{{ offer.date }}</td>
              <td>{{ offer.position }}</td>
              <td>{{ offer.salary }}</td>
              <td>
                <a :href="offer.link" target="_blank">сайт работодателя</a><br />
                <span class="badge bg-warning mt-1">In Review</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { store } from "../../script/store.js";
</script>

<script>
export default {
  name: "Dashboard",
  methods: {
    incrementNumber() {
      if (this.number < 20) {
        this.number += 1;
      }
    },
    decrementNumber() {
      if (this.number > 0) {
        this.number -= 1;
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
.counter {
  min-height: 100px;
}
.number {
  font-size: clamp(2rem, 9vw, 70px) !important;
}

.card {
  height: 325px;
}

.card-title {
  font-size: 1.5rem;
}

.table-light {
  background-color: #f8f9fa;
}

.table-responsive {
  max-height: 300px;
  overflow-y: auto;
}
</style>
 -->

 <template>
  <div class="p-4 bg-light min-vh-100">
    <h2 class="mb-4">Dashboard</h2>

    <!-- Mode Toggle Section -->
    <div class="bg-white rounded-4 border p-4 p-md-5 mb-5 shadow-sm">
      <div class="d-flex flex-column align-items-center mb-4 gap-3">
        <div class="d-flex align-items-center gap-3 flex-wrap position-relative justify-content-center">
          <span class="fw-semibold">Режим подбора:</span>

          <div class="btn-group" role="group">
            <button
              type="button"
              class="btn"
              :class="isAutoMode ? 'btn-outline-secondary' : 'btn-primary'"
              @click="isAutoMode = false"
            >
              Ручной
            </button>
            <button
              type="button"
              class="btn"
              :class="isAutoMode ? 'btn-primary' : 'btn-outline-secondary'"
              @click="isAutoMode = true"
            >
              Авто
            </button>
          </div>

          <!-- Tooltip -->
          <font-awesome-icon
            icon="question-circle"
            class="text-muted ms-2 cursor-pointer"
            @mouseenter="showTooltip = true"
            @mouseleave="showTooltip = false"
          />
          <transition name="fade">
            <div
              v-if="showTooltip"
              class="tooltip-custom"
            >
              В ручном режиме вы выбираете понравившиеся вакансии. В авто — система ищет их за вас.
            </div>
          </transition>
        </div>
      </div>

      <!-- Count and Button -->
      <div class="text-center mb-5">
        <h5 class="mb-3 h3">Сколько предложений хотите получить?</h5>
        <div class="d-flex align-items-center justify-content-center counter mb-3 flex-wrap">
          <button
            class="btn btn-outline-primary rounded-circle px-3 py-2"
            @click="decrementNumber"
            :disabled="store.userFilledData === false"
          >
            <font-awesome-icon :icon="['fas', 'angle-left']" />
          </button>

          <span class="fs-1 px-5 number">{{ number }}</span>

          <button
            class="btn btn-outline-primary rounded-circle px-3 py-2"
            @click="incrementNumber"
            :disabled="store.userFilledData === false"
          >
            <font-awesome-icon :icon="['fas', 'angle-right']" />
          </button>
        </div>

        <button
          type="button"
          class="btn btn-primary btn-lg fw-bold px-5 py-2"
          :disabled="store.userFilledData === false"
          @click="searchOffers"
        >
          Найти вакансии
        </button>

        <div v-if="store.userFilledData === false" class="text-secondary mt-3 fs-6">
          Пожалуйста, заполните данные во вкладке "О себе"
        </div>
      </div>

      <!-- Auto Mode Table or Number of Offers -->
      <div v-if="isAutoMode" class="mt-5">
        <div v-if="offers.length">
          <h5 class="text-center">Найдено {{ offers.length }} из {{ number }} вакансий</h5>
        </div>

        <div v-if="offers.length" class="table-responsive mt-4">
          <table class="table table-bordered table-hover align-middle shadow-sm">
            <thead class="table-light">
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
              <tr v-for="(offer, index) in offers" :key="offer.link">
                <td>{{ offer.company }}</td>
                <td>{{ offer.date }}</td>
                <td>{{ offer.position }}</td>
                <td>{{ offer.salary }}</td>
                <td><a :href="offer.link" target="_blank">сайт</a></td>
                <td>
                  <span class="badge bg-success mt-1">Отклик подан</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Manual Mode Cards -->
      <div v-if="!isAutoMode && offers.length" class="mt-5">
        <div class="row row-cols-1 row-cols-md-2 g-3">
          <div class="col" v-for="(offer, index) in offers" :key="offer.link">
            <div class="card shadow-sm h-100">
              <div class="card-body d-flex flex-column justify-content-between">
                <h5 class="card-title">{{ offer.position }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ offer.company }}</h6>
                <p class="card-text mb-2"><strong>Зарплата:</strong> {{ offer.salary }}</p>
                <p class="card-text mb-2"><strong>Дата:</strong> {{ offer.date }}</p>
                <div class="form-check mb-3">
                  <input class="form-check-input" type="checkbox" v-model="offer.selected" :id="'chk' + index" />
                  <label class="form-check-label" :for="'chk' + index">Выбрать</label>
                </div>
                <a :href="offer.link" class="btn btn-outline-primary mt-auto" target="_blank">Подробнее</a>
              </div>
            </div>
          </div>
        </div>
        <div class="text-end mt-4">
          <button class="btn btn-primary" @click="submitSelected">Отправить отклики</button>
        </div>
      </div>
    </div>

    <!-- Analytics Section -->
    <div class="row g-4 justify-content-center">
      <div class="col-12 col-md-6">
        <div class="card p-4 text-center shadow-sm h-100">
          <h5 class="card-title mb-3">Прогресс</h5>
          <div class="text-muted">
            <font-awesome-icon :icon="['fas', 'chart-line']" size="3x" class="mb-2" />
            <p>График прогресса появится здесь.</p>
          </div>
        </div>
      </div>

      <div class="col-12 col-md-6">
        <div class="card p-4 text-center shadow-sm h-100">
          <h5 class="card-title mb-3">Аналитика</h5>
          <div class="text-muted">
            <font-awesome-icon :icon="['fas', 'chart-pie']" size="3x" class="mb-2" />
            <p>Общая статистика будет доступна здесь.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { store } from "../../script/store.js";
</script>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      number: 3,
      isAutoMode: false,
      offers: [
        { company: "amoCRM", date: "15 Dec 2024", position: "Frontend Developer", salary: "до 50 000 ₽", link: "https://hh.ru/vacancy/111898417" },
        { company: "Yandex", date: "20 Dec 2024", position: "Junior React Dev", salary: "до 60 000 ₽", link: "https://hh.ru/vacancy/123456789" }
      ],
      showTooltip: false,
    };
  },
  methods: {
    incrementNumber() {
      if (this.number < 20) this.number++;
    },
    decrementNumber() {
      if (this.number > 1) this.number--;
    },
    async searchOffers() {
      this.offers = [
        { company: "amoCRM", date: "15 Dec 2024", position: "Frontend Developer", salary: "до 50 000 ₽", link: "https://hh.ru/vacancy/111898417" },
        { company: "Yandex", date: "20 Dec 2024", position: "Junior React Dev", salary: "до 60 000 ₽", link: "https://hh.ru/vacancy/123456789" }
      ];
    },
    submitSelected() {
      const selected = this.offers.filter(o => o.selected);
      alert(`Вы откликнулись на ${selected.length} вакансии.`);
    }
  }
};
</script>

<style scoped>
.counter {
  min-height: 100px;
}
.number {
  font-size: clamp(2rem, 9vw, 70px) !important;
}
.table-responsive {
  max-height: 300px;
  overflow-y: auto;
}
.btn-group .btn {
  min-width: 90px;
  font-weight: 500;
}
.tooltip-custom {
  position: absolute;
  top: 130%;
  left: 50%;
  z-index: 10;
  background: #fff;
  padding: 10px 14px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 250px;
  border: 1px solid #ddd;
  font-size: 0.875rem;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
hr.my-4 {
  border-top: 2px solid #ddd;
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>
