<template>
  <div class="hello">
    <button type="button" class="btn btn-primary">{{ msg }}</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: "Hello"
    }
  },
  methods : {
    getResponse() {
      const path = "http://127.0.0.1:5000/";
      axios.get(path)
      .then((res) => {
        console.log(res.data)
        this.msg = res.data;
      })
      .catch ((err) => {
        console.error(err);
      })
    }
  },
  created(){
    this.getResponse();
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
