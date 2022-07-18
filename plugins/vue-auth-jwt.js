import Vue from 'vue'
import Auth from 'vue-auth-jwt'

const config = {
  API_BASE_URL: 'https://127.0.0.1:8000/',
}

export default (context, inject) => {
  Vue.use(Auth, { config, router: context.app.router, store: context.store })
}
