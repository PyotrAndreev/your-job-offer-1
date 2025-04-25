// store.js
import { reactive } from 'vue'

export const store = reactive({
  baseUrl: "http://127.0.0.1:8000/",
  userFilledData: false,
  userAuthorizedWithHH: false,
  applicationsToFind: 0,
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
})