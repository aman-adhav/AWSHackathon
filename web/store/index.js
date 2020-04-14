export function state() {
  return {
    authenticated: false,
    user: null,
    userType: null,
    pageTitle: null
  };
}

export const mutations = {
  setAuthenticated(state, isAuthenticated) {
    state.authenticated = isAuthenticated;
  },
  setUser(state, user) {
    state.user = user;
  },
  setUserType(state, type) {
    state.userType = type;
  },
  setPageTitle(state, title) {
    state.pageTitle = title;
  }
};
