import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap'

/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { fas } from '@fortawesome/free-solid-svg-icons'

/* add icons to the library */
library.add(fas)

// createApp(App).use(router).use(VueGoogleCharts).component('font-awesome-icon', FontAwesomeIcon).mount('#app')

createApp(App).use(router).component('font-awesome-icon', FontAwesomeIcon).mount('#app')

