export default function({ store, redirect, route }) {
  if (!store.state.loggedIn) {
    return redirect(302, "/", { from: route.fullPath });
    // error({
    //   message: "You are not logged in",
    //   statusCode: 403
    // });
  }
}
