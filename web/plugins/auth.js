import {
  CognitoUserPool,
  CognitoUser,
  AuthenticationDetails
} from "amazon-cognito-identity-js";

const vendorPool = new CognitoUserPool({
  UserPoolId: process.env.VENDOR_COGNITO_POOL_ID, // Your user pool id here
  ClientId: process.env.VENDOR_COGNITO_CLIENT_ID // Your client id here
});

const deliveryPool = new CognitoUserPool({
  UserPoolId: process.env.DELIVERY_COGNITO_POOL_ID, // Your user pool id here
  ClientId: process.env.DELIVERY_COGNITO_CLIENT_ID // Your client id here
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

    if (!authenticated) this.logout();
    else this.store.commit("setAuthenticated", true);

    return authenticated;
  }

  logout() {
    this.user = null;
    this.session = null;
    this.accessToken = null;
    this.idToken = null;
    this.refreshToken = null;

    this.store.commit("setAuthenticated", false);
    this.store.commit("setUser", null);
  }

  login(username, password, userType) {
    const authenticationData = {
      Username: username,
      Password: password
    };

    const userPool = userType === "vendor" ? vendorPool : deliveryPool;

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
          this.store.commit("setUser", cognitoUser.getUsername());

          resolve(true);
        },

        onFailure: error => {
          this.logout();
          reject(error);
        },

        newPasswordRequired: (userAttributes, requiredAttributes) => {
          this.user = cognitoUser;

          delete userAttributes.email_verified;

          resolve(userAttributes);
        }
      });
    });
  }

  handleNewPassword(newPassword, userAttributes) {
    return new Promise((resolve, reject) => {
      this.user.completeNewPasswordChallenge(newPassword, userAttributes, {
        onSuccess: result => {
          this.session = result;
          this.accessToken = result.getAccessToken().getJwtToken();
          this.idToken = result.getIdToken().getJwtToken();
          this.refreshToken = result.getRefreshToken().getToken();

          this.store.commit("setAuthenticated", true);
          this.store.commit("setUser", this.user.getUsername());

          resolve(true);
        },

        onFailure: error => {
          this.logout();
          reject(error);
        }
      });
    });
  }
}

export default ({ store }, inject) => {
  inject("auth", new AuthService(store));
};
