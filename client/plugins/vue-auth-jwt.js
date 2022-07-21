import axios from "axios"
import Vue from 'vue'
import Auth from 'vue-auth-jwt'

const config = {
  API_BASE_URL: "/api/auth",
}

export default (context, inject) => {
  Vue.use(Auth, { config, router: context.app.router, store: context.store })
}
