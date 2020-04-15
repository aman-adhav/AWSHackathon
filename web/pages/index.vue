<template>
  <app-layout>
    <v-container fluid fill-height>
      <v-layout fill-height align-center justify-center>
        <v-flex>
          <v-card class="mx-auto" max-width="500">
            <v-card-title class="headline primary white--text">
              Login
            </v-card-title>
            <v-window touchless v-model="window">
              <v-window-item :value="1">
                <v-card class="border-0">
                  <v-flex shrink class="pa-4">
                    <v-flex class="text-center" shrink>
                      <v-icon
                        size="128"
                        color="primary"
                        v-text="mdiAccountCircle"
                      ></v-icon>
                    </v-flex>
                    <v-flex shrink class="pt-2 text-center">
                      <v-btn @click="loginCustomer" depressed color="primary">
                        Continue as a customer
                      </v-btn>
                    </v-flex>
                  </v-flex>
                  <v-divider></v-divider>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" text @click="window = 2">
                      Vendor/delivery login
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-window-item>
              <v-window-item :value="2">
                <v-form @submit="login" ref="form" lazy-validation>
                  <v-container class="pa-4" fluid grid-list-md>
                    <v-item-group mandatory v-model="type">
                      <v-layout>
                        <v-flex>
                          <v-item v-slot:default="{ active, toggle }">
                            <v-card
                              :class="{ 'active-login-card': active }"
                              outlined
                              @click="toggle"
                            >
                              <v-flex class="text-center pt-4 pb-0" grow>
                                <v-icon
                                  size="64"
                                  color="primary"
                                  v-text="mdiTruck"
                                ></v-icon>
                              </v-flex>
                              <v-card-title>
                                <div class="w-100 text-break text-center">
                                  Delivery login
                                </div>
                              </v-card-title>
                            </v-card>
                          </v-item>
                        </v-flex>
                        <v-flex>
                          <v-item v-slot:default="{ active, toggle }">
                            <v-card
                              :class="{ 'active-login-card': active }"
                              outlined
                              @click="toggle"
                            >
                              <v-flex class="text-center pt-4 pb-0" grow>
                                <v-icon
                                  size="64"
                                  color="primary"
                                  v-text="mdiStore"
                                ></v-icon>
                              </v-flex>
                              <v-card-title>
                                <div class="w-100 text-break text-center">
                                  Vendor login
                                </div>
                              </v-card-title>
                            </v-card>
                          </v-item>
                        </v-flex>
                      </v-layout>
                    </v-item-group>
                    <v-layout wrap>
                      <v-flex xs12>
                        <v-text-field
                          v-model="username"
                          :disabled="loading"
                          :prepend-icon="mdiAccount"
                          :rules="[rules.required]"
                          autocapitalize="off"
                          label="Username"
                        ></v-text-field>
                      </v-flex>
                      <v-flex xs12>
                        <v-text-field
                          v-model="password"
                          :prepend-icon="mdiLock"
                          :disabled="loading"
                          :rules="[rules.required, rules.min]"
                          type="password"
                          label="Password"
                        ></v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>
                  <v-divider></v-divider>
                  <v-card-actions>
                    <v-btn color="primary" text @click="window = 1">back</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                      type="submit"
                      :disabled="loading"
                      :loading="loading"
                      color="primary"
                      :state="'error'"
                      >Login</v-btn
                    >
                  </v-card-actions>
                </v-form>
              </v-window-item>
              <v-window-item :value="3">
                <v-card-title>Set a new password</v-card-title>
                <v-form
                  @submit="setNewPassword"
                  ref="newPasswordForm"
                  lazy-validation
                >
                  <v-container class="pt-0 px-4 pb-4" fluid grid-list-md>
                    <v-layout>
                      <v-flex>
                        <v-text-field
                          type="password"
                          v-model="newPassword"
                          :disabled="loading"
                          :prepend-icon="mdiLock"
                          :rules="[rules.required]"
                          autocapitalize="off"
                          label="Password"
                        ></v-text-field>
                      </v-flex>
                    </v-layout>
                  </v-container>
                  <v-divider></v-divider>
                  <v-card-actions>
                    <v-btn color="primary" text @click="window = 2">back</v-btn>
                    <v-spacer></v-spacer>
                    <v-btn
                      type="submit"
                      :disabled="loading"
                      :loading="loading"
                      color="primary"
                      :state="'error'"
                      >Submit</v-btn
                    >
                  </v-card-actions>
                </v-form>
              </v-window-item>
            </v-window>
          </v-card>
        </v-flex>
      </v-layout>
      <v-snackbar :color="snackbar.color" v-model="snackbar.on">
        {{ snackbar.text }}
        <v-btn text @click="snackbar.on = false">close</v-btn>
      </v-snackbar>
    </v-container>
  </app-layout>
</template>

<style lang="scss">
.active-login-card {
  // border: 2px solid $primary !important;
  border-color: $primary !important;
  background-color: rgba(0, 0, 0, 0.1) !important;
}
</style>

<script>
import AppLayout from "~/components/Layout/app.vue";

import {
  mdiAccount,
  mdiLock,
  mdiTruck,
  mdiAccountCircle,
  mdiStore,
  mdiChevronRight
} from "@mdi/js";

export default {
  middleware({ store, redirect }) {
    if (!store.state.authenticated) return;

    if (store.state.userType === "customer") return redirect("/complaint");

    redirect(store.state.userType === "vendor" ? "/orders" : "/deliver");
  },
  head() {
    this.$store.commit("setPageTitle", null);

    return {
      title: "Login"
    };
  },
  data() {
    return {
      snackbar: {
        color: "error",
        on: false,
        text: ""
      },
      type: 0,
      rules: {
        required: value => !!value || "Required.",
        min: v => v.length >= 6 || "Min 6 characters."
      },
      username: "",
      password: "",
      newPassword: "",
      loading: false,
      window: 1,
      mdiAccount,
      mdiLock,
      mdiTruck,
      mdiAccountCircle,
      mdiStore
    };
  },
  methods: {
    loginCustomer() {
      this.$store.commit("setAuthenticated", true);
      this.$store.commit("setUserType", "customer");
      this.$router.replace("/complaint");
    },
    login(event) {
      event.preventDefault();

      if (!this.$refs.form.validate()) return;

      this.loading = true;

      this.userType = this.type === 0 ? "delivery" : "vendor";

      this.$auth
        .login(this.username, this.password, this.userType)
        .then(response => {
          if (response !== true) {
            this.loading = false;
            this.window = 3;
            this.userAttributes = response;
            return;
          }

          this.$store.commit("setUserType", this.userType);
          this.$router.replace(
            this.userType === "vendor" ? "/orders" : "/deliver"
          );
        })
        .catch(error => {
          this.loading = false;
          console.error(error);
          this.snackbar.on = true;
          this.snackbar.text = error.message || "Couldn't login";
        });
    },
    setNewPassword(event) {
      event.preventDefault();

      if (!this.$refs.newPasswordForm.validate()) return;

      this.loading = true;

      this.$auth
        .handleNewPassword(this.newPassword, this.userAttributes)
        .then(() => {
          this.$store.commit("setUserType", this.userType);
          this.$router.replace(
            this.userType === "vendor" ? "/orders" : "/deliver"
          );
        })
        .catch(error => {
          this.loading = false;
          console.error(error);
          this.snackbar.on = true;
          this.snackbar.text = error.message || "Couldn't update password";
        });
    }
  },
  components: { AppLayout }
};
</script>