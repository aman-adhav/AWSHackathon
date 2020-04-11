export function state() {
  return {
    authenticated: false
  };
}

export const mutations = {
  setAuthenticated(state, isAuthenticated) {
    state.authenticated = isAuthenticated;
  }
};
