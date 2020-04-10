<template>
  <v-container fill-height>
    <v-layout fill-height align-center>
      <v-flex>
        <div class="display-4" v-text="error.statusCode"></div>
        <div class="display-1 font-weight-light" v-text="message"></div>
        <nuxt-link to="/">
          Home page
        </nuxt-link>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  props: {
    error: {
      type: Object,
      default: null
    }
  },
  computed: {
    message() {
      return this.error.message || "An error occurred";
    }
  },
  data() {
    return {
      pageNotFound: "404 Not Found",
      otherError: "An error occurred"
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
