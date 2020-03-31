<template>
  <app-layout title="Register product">
    <v-container class="pa-4">
      <v-card :disabled="uploading">
        <v-card-title class="headline pb-0">Info:</v-card-title>
        <v-container class="pa-4" fluid grid-list-md>
          <v-form>
            <v-layout>
              <v-flex>
                <v-text-field
                  hide-details="auto"
                  color="primary"
                  label="Title"
                ></v-text-field>
              </v-flex>
              <v-flex>
                <v-text-field
                  hide-details="auto"
                  color="primary"
                  label="Price"
                  type="number"
                  :prepend-inner-icon="mdiCurrencyUsd"
                ></v-text-field>
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex>
                <v-textarea
                  hide-details="auto"
                  color="primary"
                  label="Description"
                ></v-textarea>
              </v-flex>
            </v-layout>
            <v-layout>
              <v-flex
                ><v-text-field
                  hide-details="auto"
                  color="primary"
                  label="SKU"
                ></v-text-field
              ></v-flex>
              <v-flex
                ><v-text-field
                  hide-details="auto"
                  color="primary"
                  label="UPC"
                ></v-text-field
              ></v-flex>
              <v-flex
                ><v-text-field
                  hide-details="auto"
                  color="primary"
                  label="Inventory"
                  type="number"
                ></v-text-field
              ></v-flex>
            </v-layout>
            <v-layout wrap>
              <v-flex shrink>
                <v-checkbox
                  hide-details="auto"
                  color="primary"
                  label="Original packaging?"
                  type="checkbox"
                ></v-checkbox>
              </v-flex>
              <v-flex shrink>
                <v-checkbox
                  hide-details="auto"
                  color="primary"
                  label="Warranty?"
                  type="checkbox"
                ></v-checkbox>
              </v-flex>
            </v-layout>
          </v-form>
        </v-container>
        <v-card-title class="headline pb-0">Media:</v-card-title>
        <v-container class="pa-4" fluid>
          <app-uppy></app-uppy>
        </v-container>
        <v-divider></v-divider>
        <v-card-actions>
          <v-card-actions>
            <v-btn
              :loading="uploading"
              :success="done"
              color="primary"
              @click="upload"
              depressed
              >Upload</v-btn
            >
            <v-btn color="primary" text>Cancel</v-btn>
          </v-card-actions>
        </v-card-actions>
      </v-card>
    </v-container>
  </app-layout>
</template>

<script>
import { mdiCurrencyUsd } from "@mdi/js";

import AppLayout from "~/components/Layout/app.vue";
import AppUppy from "~/components/uppy";

import { saveProduct, saveMedia } from "~/assets/js/register";

export default {
  data() {
    return {
      uploading: false,
      done: false,
      mdiCurrencyUsd
    };
  },
  methods: {
    upload() {
      this.uploading = true;

      saveProduct()
        .then(() => saveMedia())
        .then(() => {
          this.done = true;
        })
        .finally(() => {
          this.uploading = false;
        });
    },
    saveProduct() {},
    saveMedia() {}
  },
  components: { AppLayout, AppUppy }
};
</script>