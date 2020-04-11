import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails
} from "amazon-cognito-identity-js";

const userPool = new CognitoUserPool({
  UserPoolId: process.env.COGNITO_POOL_ID, // Your user pool id here
  ClientId: process.env.COGNITO_CLIENT_ID // Your client id here
});

class AuthService {
  constructor(store) {
    this.store = store;

    this.user = null;
    this.session = null;
    this.accessToken = null;
    this.idToken = null;
    this.refreshToken = null;
  }

  isAuthenticated() {
    let authenticated = false;

    if (this.session) authenticated = this.session.isValid();

    this.store.commit("setAuthenticated", authenticated);
    return authenticated;
  }

  logout() {
    this.user = null;
    this.session = null;
    this.accessToken = null;
    this.idToken = null;
    this.refreshToken = null;

    this.store.commit("setAuthenticated", false);
  }

  login(username, password) {
    const authenticationData = {
      Username: username,
      Password: password
    };

    const userData = {
      Username: username,
      Pool: userPool
    };

    const cognitoUser = new CognitoUser(userData);

    const authenticationDetails = new AuthenticationDetails(authenticationData);

    return new Promise((resolve, reject) => {
      cognitoUser.authenticateUser(authenticationDetails, {
        onSuccess: result => {
          this.user = cognitoUser;
          this.session = result;
          this.accessToken = result.getAccessToken().getJwtToken();
          this.idToken = result.getIdToken().getJwtToken();
          this.refreshToken = result.getRefreshToken().getToken();

          this.store.commit("setAuthenticated", true);

          resolve(this.accessToken);
        },

        onFailure: error => {
          this.user = null;
          this.session = null;
          this.accessToken = null;
          this.idToken = null;
          this.refreshToken = null;

          this.store.commit("setAuthenticated", false);

          reject(error);
        }
      });
    });
  }
}

export default ({ store }, inject) => {
  inject("auth", new AuthService(store));
};
