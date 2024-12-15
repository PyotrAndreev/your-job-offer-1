<template>
  <div class="wrapper bg-light">
    <div class="container py-5">
      <h2 class="mb-4">Edit your resume</h2>
      <div class="wrapper bg-white mt-4 p-4 rounded-3 border">
        <form
          @submit.prevent="submit"
          class="align-items-center d-flex flex-column"
          id="userData"
        >
          <div class="text-center mb-4 d-flex align-items-center flex-column">
            <label
              for="image"
              class="btn btn-outline-primary rounded-circle border-primary border-2 pad"
              style="
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100px;
                height: 100px;
              "
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

            <p class="mt-2 fs-5">Upload Photo</p>
          </div>
          <div class="row g-3 w-60 row-gap-2">
            <div class="col-md-12 d-flexx justfiy-content-center">
              <label for="upload" class="form-label fw-bold">Resume</label>
              <input
                class="form-control py-2 border-2"
                type="file"
                id="upload"
                accept=".pdf"
                name="resume"
              />
            </div>
            <div class="col-md-6">
              <label for="firstName" class="form-label fw-bold"
                >First Name</label
              >
              <input
                type="text"
                class="form-control py-2 border-2"
                id="firstName"
                placeholder="Enter your first name"
                name="name"
                required
              />
            </div>
            <div class="col-md-6">
              <label for="lastName" class="form-label fw-bold">Last Name</label>
              <input
                type="text"
                class="form-control py-2 border-2"
                id="lastName"
                placeholder="Enter your last name"
              />
            </div>
            <div class="col-md-6">
              <label for="country" class="form-label fw-bold">Country</label>
              <input
                type="text"
                class="form-control py-2 border-2"
                id="country"
                placeholder="Enter your country"
              />
            </div>
            <div class="col-md-6">
              <label for="education" class="form-label fw-bold">City</label>
              <input
                type="text"
                class="form-control py-2 border-2"
                id="education"
                placeholder="Enter your city"
              />
            </div>
            <div class="col-md-6">
              <label for="country" class="form-label fw-bold">Education</label>
              <input
                type="text"
                class="form-control py-2 border-2"
                id="country"
                placeholder="Enter your education"
              />
            </div>
            <div class="col-md-6">
              <label for="education" class="form-label fw-bold">Position</label>
              <input
                type="text"
                class="form-control py-2 border-2"
                id="education"
                placeholder="Enter desired position"
              />
            </div>
            <div class="col-md-6">
              <label for="country" class="form-label fw-bold">Experience</label>
              <input
                type="text"
                class="form-control py-2 border-2"
                id="country"
                placeholder="Describe your experience"
              />
            </div>
            <div class="col-md-6">
              <label for="education" class="form-label fw-bold">Skills</label>
              <input
                type="text"
                class="form-control py-2 border-2"
                id="education"
                placeholder="Describe your skills"
              />
            </div>
            <div class="col-md-6">
              <label for="age" class="form-label fw-bold">Age</label>
              <input
                type="number"
                class="form-control py-2 border-2"
                id="age"
                placeholder="Enter your age"
              />
            </div>
            <div class="col-md-6">
              <label for="gender" class="form-label fw-bold">Gender</label>
              <select id="gender" class="form-select py-2 border-2">
                <option>Male</option>
                <option>Female</option>
              </select>
            </div>
            <div class="col-12 text-center pt-4">
              <button type="submit" class="btn btn-primary fs-5">
                Save changes
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
  methods: {
    previewImage(event) {
      const file = event.target.files[0]; // Get the selected file
      const label = event.target.parentNode; // Reference to the parent label

      if (file) {
        const reader = new FileReader();

        // Define the onload function to apply the image as background
        reader.onload = (e) => {
          label.style.backgroundImage = `url(${e.target.result})`; // Set as background image
          label.style.backgroundSize = "cover"; // Ensure the image covers the label
          label.style.backgroundPosition = "center"; // Center the image
          label.style.border = "none"; // Optionally remove border styling
        };

        // Read the file as a data URL
        reader.readAsDataURL(file);
      }
    },

    async submit() {
      const form = new FormData(document.getElementById("userData"));
      console.log(form);

      const path = "http://127.0.0.1:5000/form";
      axios
        .post(path, form)
        .then((res) => {
          console.log(res.data);
        })
        .catch((err) => {
          console.error(err);
        });
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
</style>
