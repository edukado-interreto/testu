// adapted for nuxt from https://github.com/johnckealy/vue-auth-jwt/blob/main/src/redirects.js

/* Redirects. This method checks whether a route requires authentication,
   then redirects the user to the login route if needed. */

export default async ({ route, store, redirect }) => {
  console.log("route: ", route);

  if (route.meta && route.meta[0].requiresAuth) {
    await store.dispatch("authenticator/CHECK_TOKENS");
    console.log("!!store.state.authenticator.authUser = ", !!store.state.authenticator.authUser);
    if (!!store.state.authenticator.authUser) {
      //next();
    } else {
      store.commit("authenticator/updateRedirectUrl", route.path);
      return redirect('/login')
      //next(loginFormRoute);
    }
  } else {
    //next();
  }
}
