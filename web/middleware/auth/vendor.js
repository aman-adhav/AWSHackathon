export default function({ app, store, redirect, route }) {
  if (!app.$auth.isAuthenticated() || store.state.userType !== "vendor") {
    return redirect("/");
  }
}
