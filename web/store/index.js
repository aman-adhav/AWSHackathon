export function state() {
  return {
    loggedIn: false
  };
}

export const mutations = {
  login(state) {
    this.$router.replace("/products");
    state.loggedIn = true;
  },
  logout(state) {
    state.loggedIn = false;
    this.$router.push("/");
  }
};
