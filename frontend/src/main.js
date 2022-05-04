import { createApp, Vue } from 'vue'
import App from './App.vue'
import router from './router'
import PrimeVue from 'primevue/config';
import HighchartsVue from 'highcharts-vue'

import 'primevue/resources/themes/saga-blue/theme.css'       //theme
import 'primevue/resources/primevue.min.css'                 //core css
import 'primeicons/primeicons.css';


const app = createApp(App)

app.use(router)
app.use(HighchartsVue)
app.use(PrimeVue)

app.mount('#app')