<template>
  <v-layout fill-height column>
    <v-flex v-if="title" shrink>
      <v-toolbar class="app-layout-toolbar" flat>
        <v-toolbar-title v-text="title"></v-toolbar-title>
      </v-toolbar>
    </v-flex>
    <v-flex v-if="loading" d-flex grow align-center justify-center class="app-layout-content">
      <v-progress-circular
        :size="70"
        :width="7"
        color="primary"
        indeterminate
      ></v-progress-circular>
    </v-flex>
    <v-flex v-show="!loading" grow class="app-layout-content">
      <slot></slot>
    </v-flex>
    <v-snackbar :color="snackbar.color" v-model="snackbar.on">
      {{ snackbar.text }}
      <v-btn text @click="snackbar.on = false">close</v-btn>
    </v-snackbar>
  </v-layout>
</template>

<style lang="scss">
.app-layout-toolbar {
  background: #f5f5f5 !important;
}

.app-layout-content {
  background: #fafafa;
}
</style>

<script>
export default {
  props: {
    title: String,
    snackbar: {
      type: Object,
      default() {
        return {
          color: "error",
          text: "",
          on: false
        };
      }
    },
    loading: { type: Boolean, default: false }
  }
};
</script>