import axios from "axios"
import Vue from "vue"
import Auth from "vue-auth-jwt"

const config = {
  API_BASE_URL: "/api",
  logoutEndpoint: "/auth/logout/",
  loginEndpoint: "/auth/login/",
  tokenRefreshEndpoint: "/auth/token/refresh/",
  registrationEndpoint: "/auth/register/",
  userEndpoint: "/auth/user/",
  loginRoute: "/login",
}

export default (context, inject) => {
  Vue.use(Auth, {
    config,
    router: context.app.router,
    store: context.store,
  })

  inject("auth", Vue.prototype.$auth)
  // make $auth available in asyncData
}
