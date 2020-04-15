<template>
  <v-app>
    <app-bar />
    <v-content>
      <nuxt />
    </v-content>
  </v-app>
</template>

<script>
import AppBar from "~/components/Layout/bar";

export default {
  components: { AppBar }
};
</script>
