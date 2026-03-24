import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/main.css'
import '@govbr-ds/webcomponents'
import * as DSGovComponents from '@govbr-ds/webcomponents-vue'

const app = createApp(App)

for (const [name, component] of Object.entries(DSGovComponents)) {
	if (name.startsWith('Br') && component) {
		app.component(name, component as never)
	}
}

app.use(router)

app.mount('#app')
