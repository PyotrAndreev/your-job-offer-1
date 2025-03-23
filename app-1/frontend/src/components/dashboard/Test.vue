<template>
    <div>
      <button @click="login">Login</button>
      <button @click="getProtectedData">Get Protected Data</button>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    methods: {
      async login() {
        try {
          const response = await axios.post("http://localhost:8000/token", {
            username: "test",
            password: "password",
          });
        
          localStorage.setItem("access_token", response.data.access_token);
          alert("Logged in successfully!");
        } catch (error) {
          console.error("Login error:", error);
        }
      },
      async getProtectedData() {
        try {
          const token = localStorage.getItem("access_token");
          if (!token) {
            alert("You need to log in first!");
            return;
          }
  
          const response = await axios.get("http://localhost:8000/protected", {
            headers: {
              Authorization: `Bearer ${token}`,  
            },
          });
  
          console.log("Protected data:", response.data);
        } catch (error) {
          console.error("Error accessing protected data:", error);
        }
      },
    },
  };
  </script>
  