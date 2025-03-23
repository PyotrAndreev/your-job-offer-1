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

            <p class="mt-2 fs-5">Upload Photo</p>
          </div>
          <div class="row g-3 w-60 row-gap-2">
            <div class="col-md-12 justfiy-content-center">
              <label for="upload" class="form-label ">Resume</label>
              <input
                class="form-control py-2 border-2"
                type="file"
                id="upload"
                accept=".pdf"
                name="resume"
              />
            </div>
            <div class="col-md-6">
              <label for="firstName" class="form-label "
                >First Name</label
              >
              <input
                v-model="formData.firstName"
                type="text"
                class="form-control py-2 border-2"
                id="firstName"
                placeholder="Enter your first name"
                required
              />
            </div>
            <div class="col-md-6">
              <label for="lastName" class="form-label ">Last Name</label>
              <input
                v-model="formData.lastName"
                type="text"
                class="form-control py-2 border-2"
                id="lastName"
                placeholder="Enter your last name"
              />
            </div>
            <div class="col-md-6">
              <label for="country" class="form-label ">Country</label>
              <input
                v-model="formData.country"
                type="text"
                class="form-control py-2 border-2"
                id="country"
                placeholder="Enter your country"
              />
            </div>
            <div class="col-md-6">
              <label for="education" class="form-label ">City</label>
              <input
                v-model="formData.city"
                type="text"
                class="form-control py-2 border-2"
                id="city"
                placeholder="Enter your city"
              />
            </div>
            <div class="col-md-6">
              <label for="country" class="form-label ">Education</label>
              <input
                v-model="formData.education"
                type="text"
                class="form-control py-2 border-2"
                id="education"
                placeholder="Enter your education"
              />
            </div>
            <div class="col-md-6">
              <label for="education" class="form-label ">Position</label>
              <input
                v-model="formData.position"
                type="text"
                class="form-control py-2 border-2"
                id="postition"
                placeholder="Enter desired position"
              />
            </div>
            <div class="col-md-6">
              <label for="country" class="form-label ">Experience</label>
              <input
                v-model="formData.experience"
                type="text"
                class="form-control py-2 border-2"
                id="experience"
                placeholder="Describe your experience"
              />
            </div>
            <div class="col-md-6">
              <label for="education" class="form-label ">Skills</label>
              <input
                v-model="formData.skills"
                type="text"
                class="form-control py-2 border-2"
                id="skills"
                placeholder="Describe your skills"
              />
            </div>
            <div class="col-md-6">
              <label for="age" class="form-label ">Age</label>
              <input
                v-model="formData.age"
                type="number"
                class="form-control py-2 border-2"
                id="age"
                placeholder="Enter your age"
              />
            </div>
            <div class="col-md-6">
              <label for="gender" class="form-label ">Gender</label>
              <select
                v-model="formData.gender"
                id="gender"
                class="form-select py-2 border-2"
              >
                <option value="male">Male</option>
                <option value="female">Female</option>
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
import { store } from "../../script/store.js";

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
      imagePreviewStyle: {}, // For the image preview
      userId: localStorage.getItem("user_id"), // Get user_id from localStorage
    };
  },
  methods: {
    // Preview uploaded image and save as base64
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

    // Save form data to localStorage
    saveForm() {
      localStorage.setItem("formData", JSON.stringify(this.formData));
    },

    // Submit form data to the backend
    async submit() {
      store.userFilledData = true; // Set store flag to indicate data submission
      try {
        const formData = new FormData();
        const resumeFile = document.getElementById("upload").files[0];

        if (resumeFile) {
          console.log(2)
          // alert("Please upload a resume.");
          // return;
        }

        // Append data to FormData
        if (this.userId) {
          formData.append("user_id", this.userId); // Include user_id for updates
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

        // Send data to the server
        const response = await axios.post(
          `${store.baseUrl}userData`,
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );

        console.log("Response from server:", response.data);

        const { message, user_id } = response.data;

        // Save user_id in localStorage if creating a new user
        if (!this.userId) {
          localStorage.setItem("user_id", user_id);
        }

        alert(`${message}! Welcome!`);
      } catch (error) {
        if (error.response) {
          console.error("Server responded with:", error.response.data);
          alert(`Error: ${error.response.data.detail || "Invalid request."}`);
        } else {
          console.error("Request error:", error);
          alert(
            "An error occurred while submitting the form. Please try again."
          );
        }
      }
    },

 
  },
  mounted() {
    // Load saved data from localStorage
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

    // Fetch user data from server if needed
    // this.fetchUserData();
  },
  watch: {
    formData: {
      handler: "saveForm", // Automatically save form data on change
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
</style>
