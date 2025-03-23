<template>
  <div class="wrapper d-flex vw-100 vh-100 bg-light bg-gradient">
    <div class="container pt-5 mt-5" style="max-width: 1000px">
      <div class="row justify-content-center px-4">
        <div class="col-md-6 rounded-5 p-4 bg-white">
          <h2 class="text-center pb-4">Вход</h2>
          <form @submit.prevent="login">
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
              <label for="password" class="form-label">Пароль</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="password"
                required
              />
            </div>
            <button type="submit" class="btn btn-primary w-100">Войти</button>
          </form>
          <div class="mt-3 text-center">
            <span>
              Нет аккаунта?
              <a class="px-1 text-decoration-none" href="#registration">
                Зарегистрироваться
              </a>
            </span>
          </div>
          <div v-if="errorMessage" class="alert alert-danger mt-3">
            {{ errorMessage }}
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
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      // console.log(123)
      this.$router.replace({ path: "/dashboard" });

      // if (this.username && this.password) {
      //   const path = "http://127.0.0.1:5000/login";
      //   let msg = "";
      //   await axios
      //     .post(path, {
      //       username: this.username,
      //       password: this.password,
      //     })
      //     .then(function (response) {
      //       if (response.data.access_token) {
      //         localStorage.setItem("token", response.data.access_token);
      //       }
      //     })
      //     .catch(function (err) {
      //       console.log(err);
      //       msg = err.response.data.msg;
      //     });
      //   if (msg === "") {
      //     this.$router.replace({ path: "/dashboard" });
      //   }
      //   this.errorMessage = msg;
      //   console.log(this.errorMessage);
      // } else {
      //   this.errorMessage = "Please fill in all fields";
      // }
    },
  },
};
</script>

<style scoped></style>
