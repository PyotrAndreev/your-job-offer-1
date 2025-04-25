<template>
  <div class="wrapper d-flex vw-100 vh-100 bg-light bg-gradient">
    <div class="container pt-5 mt-5" style="max-width: 1000px">
      <div class="row justify-content-center px-4">
        <div class="col-md-6 rounded-5 p-4 bg-white">
          <h2 class="text-center pb-4">Регистрация</h2>
          <form @submit.prevent="register">
            <div class="mb-3">
              <label for="username" class="form-label">Имя пользователя</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="username"
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

<script setup>
import { store } from "../script/store.js";
</script>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
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
        this.username &&
        this.email &&
        this.password &&
        this.confirmPassword
      ) {
        if (this.password !== this.confirmPassword) {
          this.errorMessage = "Passwords do not match";
          return;
        }
        //server url
        const path = store.baseUrl + 'users/';


        // await axios
        //   .post(path, {
        //     username: this.username,
        //     password: this.password,
        //   })
        //   .then(function (response) {
        //     console.log("user registered!");
        //     console.log(response);
        //   })
        //   .catch(function (err) {
        //     console.log(err);
        //   });
        // this.errorMessage = "";
        // this.username = "";
        // this.email = "";
        // this.password = "";
        // this.confirmPassword = "";

        this.Message = "Регистрация успешна! Перенаправление на страницу входа...";
        setTimeout(() => {
          this.$router.replace({ path: "/login" });
        }, 2000);
      } else {
        this.errorMessage = "Пожалуйста, заполните все поля";
      }
    },
  },
};
</script>

<style scoped></style>