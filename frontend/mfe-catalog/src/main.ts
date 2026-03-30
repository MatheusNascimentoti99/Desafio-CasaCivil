import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import CatalogCrudPage from './pages/CatalogCrudPage.vue'

const app = createApp(CatalogCrudPage)
const vuetify = createVuetify({
  components,
  directives,
})

app.use(vuetify)
app.mount('#app')
