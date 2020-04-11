export default function({ app, store, redirect, route }) {
  if (!app.$auth.isAuthenticated()) {
    return redirect(302, "/", { from: route.fullPath });
  }
}
