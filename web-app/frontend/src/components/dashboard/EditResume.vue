<template>
  <div class="wrapper bg-light">
    <div class="container py-5">
      <h2 class="mb-4 text-center text-md-start">Профиль</h2>
      <div class="wrapper bg-white mt-4 p-2 p-sm-4 rounded-3 border">
        <form
          @submit.prevent="submit"
          class="align-items-center d-flex flex-column"
          id="userData"
        >
          <div class="text-center mb-4 d-flex align-items-center flex-column">
            <label
              for="image"
              class="btn btn-outline-primary rounded-circle border-primary border-2 p-4 p-sm-5"
              :style="imagePreviewStyle"
            >
              <font-awesome-icon
                :icon="['fas', 'camera']"
                class="fs-2"
                style="cursor: pointer; color: white"
              />
              <input
                type="file"
                id="image"
                style="display: none"
                accept="image/*"
                name="photo"
                @change="previewImage"
              />
            </label>
            <p class="mt-2 fs-5">Загрузите фото</p>
          </div>

          <div class="row g-3 w-100 w-md-75 w-lg-60 mx-auto row-gap-2">
            <div class="col-md-12">
              <label for="upload" class="form-label">Загрузите pdf файл с резюме</label>
              <input
                class="form-control py-2 border-2"
                type="file"
                id="upload"
                accept=".pdf"
                name="resume"
              />
            </div>
            <div class="col-md-6">
              <label for="firstName" class="form-label">Имя</label>
              <input
                v-model="formData.firstName"
                type="text"
                class="form-control py-2 border-2"
                id="firstName"
                placeholder="Введите имя"
                required
              />
            </div>
            <div class="col-md-6">
              <label for="lastName" class="form-label">Фамилия</label>
              <input
                v-model="formData.lastName"
                type="text"
                class="form-control py-2 border-2"
                id="lastName"
                placeholder="Введите фамилию"
              />
            </div>
            <div class="col-md-6">
              <label for="country" class="form-label">Страна</label>
              <input
                v-model="formData.country"
                type="text"
                class="form-control py-2 border-2"
                id="country"
                placeholder="Укажите вашу страну"
              />
            </div>
            <div class="col-md-6">
              <label for="city" class="form-label">Город</label>
              <input
                v-model="formData.city"
                type="text"
                class="form-control py-2 border-2"
                id="city"
                placeholder="Укажите ваш город"
              />
            </div>
            <div class="col-md-6">
              <label for="education" class="form-label">Образование</label>
              <input
                v-model="formData.education"
                type="text"
                class="form-control py-2 border-2"
                id="education"
                placeholder="Укажите ваше образование"
              />
            </div>
            <div class="col-md-6">
              <label for="position" class="form-label">Должность</label>
              <input
                v-model="formData.position"
                type="text"
                class="form-control py-2 border-2"
                id="position"
                placeholder="Укажите желаемую должность"
              />
            </div>
            <div class="col-md-6">
              <label for="experience" class="form-label">Опыт</label>
              <textarea
                v-model="formData.experience"
                class="form-control py-2 border-2"
                id="experience"
                placeholder="Опишите ваш опыт"
                rows="3"
              ></textarea>
            </div>
            <div class="col-md-6">
              <label for="skills" class="form-label">Навыки</label>
              <textarea
                v-model="formData.skills"
                class="form-control py-2 border-2"
                id="skills"
                placeholder="Опишите ваши навыки"
                rows="3"
              ></textarea>
            </div>
            <div class="col-md-6">
              <label for="age" class="form-label">Возраст</label>
              <input
                v-model="formData.age"
                type="number"
                class="form-control py-2 border-2"
                id="age"
                placeholder="Укажите возраст"
              />
            </div>
            <div class="col-md-6">
              <label for="gender" class="form-label">Пол</label>
              <select
                v-model="formData.gender"
                id="gender"
                class="form-select py-2 border-2"
              >
                <option value="male">Мужской</option>
                <option value="female">Женский</option>
              </select>
            </div>
            <div class="col-12 text-center pt-4">
              <button type="submit" class="btn btn-primary fs-5">
                Сохранить изменения
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { store } from "../../script/store.js";
</script>

<script>
import axios from "axios";

export default {
  name: "EditResume",
  data() {
    return {
      formData: JSON.parse(localStorage.getItem("formData")) || {
        firstName: "",
        lastName: "",
        country: "",
        city: "",
        education: "",
        position: "",
        experience: "",
        skills: "",
        age: "",
        gender: "",
      },
      imagePreviewStyle: {},
      userId: localStorage.getItem("user_id"),
    };
  },
  methods: {
    previewImage(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.imagePreviewStyle = {
            backgroundImage: `url(${e.target.result})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            border: "none",
          };
          localStorage.setItem("imagePreview", e.target.result);
        };
        reader.readAsDataURL(file);
      }
    },
    saveForm() {
      localStorage.setItem("formData", JSON.stringify(this.formData));
    },
    async submit() {
      store.userFilledData = true;
      try {
        const formData = new FormData();
        const resumeFile = document.getElementById("upload").files[0];
        if (this.userId) {
          formData.append("user_id", this.userId);
        }
        formData.append("first_name", this.formData.firstName);
        formData.append("last_name", this.formData.lastName);
        formData.append("resume", resumeFile);
        formData.append("country", this.formData.country);
        formData.append("city", this.formData.city);
        formData.append("education", this.formData.education);
        formData.append("position", this.formData.position);
        formData.append("experience", this.formData.experience);
        formData.append("skills", this.formData.skills);
        formData.append("age", parseInt(this.formData.age, 10));
        formData.append("gender", this.formData.gender);

        const path = import.meta.env.VITE_BASE_URL + "userData";

        const response = await axios.post(path, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        alert(`${response.data.message}! Спасибо!`);
      } catch (error) {
        if (error.response) {
          alert(`Ошибка: ${error.response.data.detail || "Неверный запрос"}`);
        } else {
          alert("Что-то пошло не так, пожалуйста, попробуйте снова.");
        }
      }
    },
  },
  mounted() {
    const savedData = localStorage.getItem("formData");
    if (savedData) {
      this.formData = JSON.parse(savedData);
    }
    const savedImage = localStorage.getItem("imagePreview");
    if (savedImage) {
      this.imagePreviewStyle = {
        backgroundImage: `url(${savedImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        border: "none",
      };
    }
  },
  watch: {
    formData: {
      handler: "saveForm",
      deep: true,
    },
  },
};
</script>

<style scoped>
button.btn-outline-primary {
  width: 100px;
  height: 100px;
}

.pad {
  padding: 35px;
}

.w-60 {
  width: 60%;
}

textarea.form-control {
  resize: vertical;
}

@media (max-width: 576px) {
  .input-expandable {
    width: 100%;
  }

  button.btn-outline-primary {
    width: 80px;
    height: 80px;
  }

  textarea.form-control {
    resize: both;
    min-height: 120px;
  }
}
</style>
