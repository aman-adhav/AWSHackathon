export default function({ store, error, redirect }) {
  console.log("in middleware")
  if (!store.state.loggedIn) {
    return redirect("/");
    // error({
    //   message: "You are not logged in",
    //   statusCode: 403
    // });
  }
}
