<template>
  <v-app-bar clipped-left dark color="primary" app>
    <v-toolbar-title>
      <nuxt-link to="/" class="app-bar-title">
        <span class="font-weight-bold">amazon</span>&nbsp;Vendors
      </nuxt-link>
    </v-toolbar-title>

    <v-spacer></v-spacer>
    <v-toolbar-items v-if="$store.state.authenticated">
      <template v-if="$store.state.userType === 'vendor'">
        <template v-if="$vuetify.breakpoint.xsOnly">
          <v-menu offset-y>
            <template v-slot:activator="{ on }">
              <v-btn x-small text v-on="on">
                <v-icon v-text="mdiDotsVertical"></v-icon>
              </v-btn>
            </template>
            <v-list right>
              <v-list-item exact to="/orders">
                <v-list-item-title>View orders</v-list-item-title>
              </v-list-item>
              <v-list-item to="/products/register">
                <v-list-item-title>Register product</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
        <template v-else>
          <v-btn to="/orders" exact text>
            <v-icon v-text="mdiApps"></v-icon>
          </v-btn>
          <v-btn to="/products/register" text>
            <v-icon v-text="mdiDropbox"></v-icon>
          </v-btn>
        </template>
      </template>
      <v-menu offset-y>
        <template v-slot:activator="{ on }">
          <v-btn :x-small="$vuetify.breakpoint.xsOnly" text v-on="on">
            <v-icon v-text="mdiAccount"></v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-title>Log Out</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-toolbar-items>
  </v-app-bar>
</template>

<style lang="scss" scoped>
.app-bar-title {
  color: inherit !important;
  text-transform: none;
  text-decoration: none;
}
</style>

<script>
import { mdiAccount, mdiDotsVertical, mdiApps, mdiDropbox } from "@mdi/js";

export default {
  data() {
    return { mdiAccount, mdiDotsVertical, mdiApps, mdiDropbox };
  },
  methods: {
    logout() {
      this.$store.commit("setUserType", null);
      this.$auth.logout();
      this.$router.push("/");
    }
  }
};
</script>