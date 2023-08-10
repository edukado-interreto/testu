// adapted for nuxt from https://github.com/johnckealy/vue-auth-jwt/blob/main/src/redirects.js

/* Redirects. This method checks whether a route requires authentication,
   then redirects the user to the login route if needed. */

export default async ({ route, store, redirect, app }) => {
  if (route.meta && route.meta[0].requiresAuth) {
    await store.dispatch("authenticator/CHECK_TOKENS")
    if (!!store.state.authenticator.authUser) {
      //next();
    } else {
      store.commit("authenticator/updateRedirectUrl", route.path)
      return redirect(app.localePath("/login"))
      //next(loginFormRoute);
    }
  } else {
    //next();
  }
}
