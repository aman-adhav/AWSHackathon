export default function({ app, store, redirect, route }) {
  if (!app.$auth.isAuthenticated() || store.state.userType !== "delivery") {
    return redirect("/");
  }
}
