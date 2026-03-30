import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import '@eccc/shared-ui/styles.css'
import { createDsgovVuetifyOptions } from '@eccc/shared-ui/vuetify'
import OrdersApp from './pages/OrdersListPage.vue'

const app = createApp(OrdersApp)
const vuetify = createVuetify(
	createDsgovVuetifyOptions({
		components,
		directives,
	}),
)

app.use(vuetify)
app.mount('#app')
