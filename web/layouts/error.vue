<template>
  <v-container style="max-width: 1185px !important" fill-height>
    <v-layout class="error-container" fill-height align-center>
      <v-flex>
        <p class="display-4" v-text="error.statusCode"></p>
        <p class="display-1 font-weight-light" v-text="message"></p>
        <v-btn depressed color="primary" to="/">Home page</v-btn>
      </v-flex>
      <v-icon
        class="hidden-sm-and-down"
        size="512"
        color="grey lighten-4"
        v-text="mdiAlertCircleOutline"
      ></v-icon>
    </v-layout>
  </v-container>
</template>

<style lang="scss">
.error-container {
  position: relative;
  overflow: hidden;

  .flex {
    z-index: 2;
  }

  .v-icon {
    z-index: 1;
    position: absolute !important;
    top: 50%;
    right: 0;
    transform: translateY(-50%);
  }
}
</style>

<script>
import { mdiAlertCircleOutline } from "@mdi/js";

export default {
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  computed: {
    message() {
      if (process.env.NODE_ENV === "production") return "An error occurred";

      return this.error.message || "An error occurred";
    }
  },
  data() {
    return {
      pageNotFound: "404 Not Found",
      otherError: "An error occurred",
      mdiAlertCircleOutline
    };
  },
  head() {
    const title =
      this.error.statusCode === 404 ? this.pageNotFound : this.otherError;

    return {
      title
    };
  }
};
</script>
