<template>
  <app-layout title="Register product">
    <v-container class="pa-4">
      <v-card :disabled="uploading">
        <v-window v-model="window">
          <v-window-item :value="1">
            <v-card-title>Upload barcode</v-card-title>
            <v-card-text>
              <app-uppy
                @complete="barcodeUploaded"
                :config="{
                  restrictions: {
                    maxNumberOfFiles: 1,
                    allowedFileTypes: ['image/jpeg', 'image/png']
                  },
                  autoProceed: true
                }"
              ></app-uppy>
            </v-card-text>
          </v-window-item>
          <v-window-item :value="2">
            <v-card-title>Enter product</v-card-title>
            <v-card-subtitle class="px-4 pt-4 pb-0">
              General information:
            </v-card-subtitle>
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
            <v-card-subtitle class="pb-0">Media:</v-card-subtitle>
            <v-container class="pa-4" fluid>
              <app-uppy></app-uppy>
            </v-container>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                :loading="uploading"
                :success="done"
                color="primary"
                @click="upload"
                depressed
              >
                Upload
              </v-btn>
            </v-card-actions>
          </v-window-item>
        </v-window>
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
  middleware: "auth",
  data() {
    return {
      uploading: false,
      done: false,
      mdiCurrencyUsd,
      window: 1
    };
  },
  methods: {
    barcodeUploaded({ successful }) {
      if (!successful.length) return;

      this.window = 2;
    },
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