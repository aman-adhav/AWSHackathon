<template>
  <v-app>
    <v-app-bar clipped-left dark color="primary" app>
      <v-toolbar-title>
        <span class="font-weight-bold">amazon</span>&nbsp;Vendors
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <v-toolbar-items v-if="$store.state.loggedIn">
        <v-btn to="/products" exact text>
          <v-icon v-text="mdiApps"></v-icon>
        </v-btn>
        <v-btn to="/products/register" text>
          <v-icon v-text="mdiDropbox"></v-icon>
        </v-btn>
        <v-menu offset-y>
          <template v-slot:activator="{ on }">
            <v-btn text v-on="on">
              <v-icon v-text="mdiAccount"></v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="$store.commit('logout')">
              <v-list-item-title>Log Out</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar-items>
    </v-app-bar>
    <v-content>
      <nuxt />
    </v-content>
  </v-app>
</template>

<script>
import { mdiAccount, mdiApps, mdiDropbox } from "@mdi/js";

export default {
  data() {
    return { mdiAccount, mdiApps, mdiDropbox };
  }
};
</script>
