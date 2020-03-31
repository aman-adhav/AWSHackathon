<template>
  <v-layout fill-height column>
    <v-flex v-if="title" shrink>
      <v-toolbar class="app-layout-toolbar" flat>
        <v-toolbar-title v-text="title"></v-toolbar-title>
      </v-toolbar>
    </v-flex>
    <v-flex grow class="app-layout-content"><slot></slot></v-flex>
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
    title: String
  }
};
</script>