export function state() {
  return {
    authenticated: false,
    user: null
  };
}

export const mutations = {
  setAuthenticated(state, isAuthenticated) {
    state.authenticated = isAuthenticated;
  },
  setUser(state, user) {
    state.user = user;
  }
};
