export default function({ app, store, redirect, route }) {
  if (!store.state.authenticated || store.state.userType !== "customer") {
    return redirect("/");
  }
}
