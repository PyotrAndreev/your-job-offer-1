<template>
  <div class="wrapper d-flex vw-100 vh-100 bg-light bg-gradient">
    <div class="container pt-5 mt-5" style="max-width: 1000px">
      <div class="row justify-content-center px-4">
        <div class="col-md-6 rounded-5 p-4 bg-white">
          <h2 class="text-center pb-4">Регистрация</h2>
          <form @submit.prevent="register">
            <div class="mb-3">
              <label for="phoneNumber" class="form-label">Номер телефона</label>
              <input
                type="tel"
                class="form-control"
                id="phoneNumber"
                v-model="phoneNumber"
                required
              />
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Почта</label>
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="email"
                required
              />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Пароль</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="password"
                required
              />
            </div>
            <div class="mb-3">
              <label for="confirmPassword" class="form-label"
                >Подтверждение пароля</label
              >
              <input
                type="password"
                class="form-control"
                id="confirmPassword"
                v-model="confirmPassword"
                required
              />
            </div>
            <button type="submit" class="btn btn-primary w-100">
              Зарегистрироваться
            </button>
          </form>
          <div class="mt-3 text-center">
            <span>
              Уже есть аккаунт?
              <a class="px-1 text-decoration-none" href="login">Войти</a>
            </span>
          </div>
          <div v-if="errorMessage" class="alert alert-danger mt-3">
            {{ errorMessage }}
          </div>
          <div v-if="Message" class="alert alert-success mt-3">
            {{ Message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      phoneNumber: "",
      email: "",
      password: "",
      confirmPassword: "",
      errorMessage: "",
      Message: "",
    };
  },
  methods: {
    async register() {
      if (
        this.phoneNumber &&
        this.email &&
        this.password &&
        this.confirmPassword
      ) {

        if (!/^(\+7)\d{10}$/.test(this.phoneNumber)) {
          this.errorMessage = "Введите номер в формате - +7XXXXXXXXXX";
          return;
        }

        if (this.password !== this.confirmPassword) {
          this.errorMessage = "Пароли не совпадают";
          return;
        }

        const path = import.meta.env.VITE_BASE_URL + "registration"

        await axios
          .post(path, {
            phoneNumber: this.phoneNumber,
            email: this.email,
            password: this.password
          })
          .then((response) => {
            localStorage.setItem("user_id", response.data.user_id); 
            console.log("user registered!");
          })
          .catch((err) => {
            console.log(err);
          });
        this.errorMessage = "";
        this.phoneNumber = "";
        this.email = "";
        this.password = "";
        this.confirmPassword = "";

        this.Message = "Регистрация успешна! Перенаправление на страницу входа...";
        setTimeout(() => {
          this.$router.replace({ path: "/login" });
        }, 1000);
      } else {
        this.errorMessage = "Пожалуйста, заполните все поля";
      }
    },
  },
};
</script>

<style scoped></style>