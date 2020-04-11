<template>
  <v-container fluid fill-height>
    <v-layout fill-height align-center justify-center>
      <v-flex shrink>
        <v-card max-width="500">
          <v-card-title class="headline primary white--text"
            >Login</v-card-title
          >
          <v-form ref="form" lazy-validation>
            <v-container fluid grid-list-md>
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
          </v-form>
          <v-card-actions right>
            <v-spacer></v-spacer>
            <v-btn
              @click="login"
              :disabled="loading"
              :loading="loading"
              color="primary"
              :state="'error'"
              >Login</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
    <v-snackbar :color="snackbar.color" v-model="snackbar.on">
      {{ snackbar.text }}
      <v-btn text @click="snackbar.on = false">close</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
import { mdiAccount, mdiLock, mdiClose } from "@mdi/js";

export default {
  middleware({ store, redirect, query }) {
    const { from } = query;

    if (store.state.loggedIn) return redirect(from || "/products");
  },
  data() {
    return {
      snackbar: {
        color: "error",
        on: false,
        text: ""
      },
      rules: {
        required: value => !!value || "Required.",
        min: v => v.length >= 8 || "Min 6 characters."
      },
      username: "",
      password: "",
      loading: false,
      mdiAccount,
      mdiLock,
      mdiClose
    };
  },
  methods: {
    login() {
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