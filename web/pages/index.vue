<template>
  <v-container fluid fill-height>
    <v-layout fill-height align-center justify-center>
      <v-flex>
        <v-card class="mx-auto" max-width="500">
          <v-card-title class="headline primary white--text">
            Login
          </v-card-title>
          <v-window v-model="window">
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
                    <v-btn depressed color="primary">
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
                <v-container fluid grid-list-md>
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
                <v-card-actions right>
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
          </v-window>
        </v-card>
      </v-flex>
    </v-layout>
    <v-snackbar :color="snackbar.color" v-model="snackbar.on">
      {{ snackbar.text }}
      <v-btn text @click="snackbar.on = false">close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<style lang="scss">
.active-login-card {
  // border: 2px solid $primary !important;
  border-color: $primary !important;
}
</style>

<script>
import {
  mdiAccount,
  mdiLock,
  mdiTruck,
  mdiAccountCircle,
  mdiStore,
  mdiChevronRight
} from "@mdi/js";

export default {
  middleware({ store, redirect, query }) {
    const { from } = query;

    if (store.state.authenticated) redirect(from || "/products");
  },
  data() {
    return {
      snackbar: {
        color: "error",
        on: false,
        text: ""
      },
      type: -1,
      rules: {
        required: value => !!value || "Required.",
        min: v => v.length >= 6 || "Min 6 characters."
      },
      username: "",
      password: "",
      loading: false,
      window: 1,
      mdiAccount,
      mdiLock,
      mdiTruck,
      mdiAccountCircle,
      mdiStore
    };
  },
  watch: {
    type(val) {
      console.log(val);
    }
  },
  methods: {
    login(event) {
      event.preventDefault();

      if (!this.$refs.form.validate()) return;

      this.loading = true;

      this.$auth
        .login(this.username, this.password)
        .then(token => {
          const { from } = this.$route.query;

          this.$router.push(from || "/products");
        })
        .catch(error => {
          this.loading = false;
          console.error(error);
          this.snackbar.on = true;
          this.snackbar.text = error.message || "Couldn't login";
        });

      // auth(this.username, this.password)
      //   .then(token => console.log(token))
      //   .catch(error => console.error(error));

      // this.$store.commit("login");

      // const { from } = this.$route.query;

      // this.$router.push(from || "/products");
    }
  }
};
</script>