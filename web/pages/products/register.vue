<template>
  <app-layout :snackbar="snackbar" title="Register product">
    <v-container class="pa-4">
      <v-card :disabled="uploading">
        <v-window touchless v-model="window">
          <v-window-item :value="1">
            <v-card-title>Upload barcode</v-card-title>
            <v-card-text>
              <app-uppy
                ref="barcodeUppy"
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
                      v-model="title"
                      :readonly="createdProduct"
                      hide-details="auto"
                      color="primary"
                      label="Title"
                    ></v-text-field>
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      v-model="price"
                      :readonly="createdProduct"
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
                      v-model="desc"
                      :readonly="createdProduct"
                      hide-details="auto"
                      color="primary"
                      label="Description"
                    ></v-textarea>
                  </v-flex>
                </v-layout>
                <v-layout>
                  <v-flex>
                    <v-text-field
                      v-model="sku"
                      :readonly="createdProduct"
                      hide-details="auto"
                      color="primary"
                      label="SKU"
                    >
                    </v-text-field>
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      hide-details="auto"
                      color="primary"
                      label="UPC"
                      v-model="upc"
                      :readonly="createdProduct"
                    >
                    </v-text-field>
                  </v-flex>
                  <v-flex>
                    <v-text-field
                      hide-details="auto"
                      color="primary"
                      label="Inventory"
                      type="number"
                      v-model="inventory"
                      :readonly="createdProduct"
                    >
                    </v-text-field>
                  </v-flex>
                </v-layout>
                <v-layout wrap>
                  <v-flex shrink>
                    <v-checkbox
                      hide-details="auto"
                      color="primary"
                      label="Original packaging?"
                      type="checkbox"
                      v-model="packaging"
                      :readonly="createdProduct"
                    ></v-checkbox>
                  </v-flex>
                  <v-flex shrink>
                    <v-checkbox
                      hide-details="auto"
                      color="primary"
                      label="Warranty?"
                      type="checkbox"
                      v-model="warranty"
                      :readonly="createdProduct"
                    ></v-checkbox>
                  </v-flex>
                </v-layout>
              </v-form>
            </v-container>
            <v-card-subtitle class="pb-0">Media:</v-card-subtitle>
            <v-container class="pa-4" fluid>
              <app-uppy ref="mediaUppy"></app-uppy>
            </v-container>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                :loading="uploading"
                color="primary"
                @click="upload"
                depressed
              >
                Upload
              </v-btn>
            </v-card-actions>
          </v-window-item>
          <v-window-item :value="3">
            <v-card>
              <v-flex grow class="pa-4 text-center">
                <v-icon
                  v-if="!fake"
                  color="success"
                  size="100"
                  v-text="mdiCheckCircle"
                >
                </v-icon>
                <v-icon v-else color="error" size="100" v-text="mdiClose">
                </v-icon>
              </v-flex>
              <v-card-title class="justify-center">
                <span class="text-break text-center" v-text="message"></span>
              </v-card-title>
              <v-card-actions class="justify-center">
                <v-btn color="primary" text @click="goHome">
                  go home
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-window-item>
        </v-window>
      </v-card>
    </v-container>
  </app-layout>
</template>

<script>
import { mdiCurrencyUsd, mdiCheckCircle, mdiClose } from "@mdi/js";

import AppLayout from "~/components/Layout/app.vue";
import AppUppy from "~/components/uppy";

export default {
  middleware: "auth/vendor",
  head() {
    this.$store.commit("setPageTitle", "Register product");

    return {
      title: this.$store.state.pageTitle
    };
  },
  data() {
    return {
      uploading: false,
      createdProduct: false,
      mdiCurrencyUsd,
      mdiCheckCircle,
      mdiClose,
      window: 1,
      title: null,
      price: null,
      desc: null,
      sku: null,
      upc: null,
      inventory: null,
      packaging: false,
      warranty: false,
      id: null,
      uploadedMedia: false,
      message: "",
      fake: false,
      snackbar: {
        on: false,
        text: "",
        color: "error"
      }
    };
  },
  mounted() {
    this.$refs.barcodeUppy.uppy.getPlugin("XHRUpload").opts.endpoint =
      // "https://dummy.restapiexample.com/api/v1/create";
      "http://localhost:5000/scan_barcode";
  },
  methods: {
    goHome() {
      this.$router.push("/orders");
    },
    barcodeUploaded({ successful }) {
      if (!successful.length) return;

      const { body } = successful[0].response;

      if (body.barcode) this.upc = body.barcode;
      if (body.price) this.price = body.price;
      if (body.product_name) this.title = body.product_name;
      this.id = body.product_id;

      this.window = 2;
    },
    upload() {
      this.uploading = true;

      if (this.uploadedMedia) return this.sendForReview();

      // title: null,
      // price: null,
      // desc: null,
      // sku: null,
      // upc: null,
      // inventory: null,
      // packaging: false,
      // warranty: false,
      // id: null

      // const product = {
      //   id: this.id,
      //   title: this.title,
      //   price: this.price,
      //   desc: this.desc,
      //   sku: this.sku,
      //   upc: this.upc,
      //   inventory: this.inventory,
      //   packaging: this.packaging,
      //   warranty: this.warranty
      // };

      const product = {
        product_name: this.title,
        product_price: Number.parseFloat(this.price),
        is_used_product: this.packaging,
        barcode: this.upc,
        product_description: this.desc,
        stat: "unfulfilled"
      };

      let promise;
      if (this.createdProduct) promise = this.$refs.mediaUppy.upload();
      else
        promise = this.$axios({
          method: "POST",
          url: `http://localhost:5000/update/${this.id}`,
          data: product
        }).then(({ data }) => {
          this.createdProduct = true;

          this.$refs.mediaUppy.uppy.getPlugin(
            "XHRUpload"
          ).opts.endpoint = `http://localhost:5000/upload/${this.id}`;

          return this.$refs.mediaUppy.upload();
        });

      promise
        .then(({ failed }) => {
          if (failed.length) return;

          this.uploadedMedia = true;

          return this.sendForReview();
        })
        .catch(error => {
          this.snackbar.text = error.message || "Couldn't add product";
          this.snackbar.on = true;
        })
        .finally(() => {
          this.uploading = false;
        });
    },
    sendForReview() {
      return this.$axios({
        method: "POST",
        url: `http://localhost:5000/send_for_review/${this.id}`
      }).then(({ data }) => {
        console.log(data);

        if (data.fake_product_message === "All Clear") {
          this.message = "Created new product";
          this.fake = false;
        } else {
          this.message = data.fake_product_message;
          this.fake = true;
        }

        this.window = 3;
      });
    }
  },
  components: { AppLayout, AppUppy }
};
</script>