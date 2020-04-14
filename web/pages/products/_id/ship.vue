<template>
  <app-layout title="Ship product">
    <v-container class="pa-4">
      <v-card>
        <v-window v-model="window">
          <v-window-item :value="1">
            <v-card-title>Review information</v-card-title>
            <v-card-subtitle class="px-4 pt-4 pb-0">Personal:</v-card-subtitle>
            <v-container class="pa-4" fluid grid-list-md>
              <v-layout wrap>
                <v-flex>
                  <v-text-field
                    hide-details
                    :value="name"
                    color="primary"
                    label="Name"
                    readonly
                  />
                </v-flex>
                <v-flex>
                  <v-text-field
                    hide-details
                    :value="phone"
                    color="primary"
                    label="Phone"
                    readonly
                  />
                </v-flex>
                <v-flex>
                  <v-text-field
                    hide-details
                    :value="email"
                    color="primary"
                    label="Email"
                    readonly
                  />
                </v-flex>
              </v-layout>
            </v-container>
            <v-card-subtitle class="pb-0">Shipping:</v-card-subtitle>
            <v-container class="pa-4" fluid grid-list-md>
              <v-layout wrap>
                <v-flex>
                  <v-text-field
                    hide-details
                    :value="address"
                    color="primary"
                    label="Address"
                    readonly
                  />
                </v-flex>
                <v-flex>
                  <v-text-field
                    hide-details
                    :value="city"
                    color="primary"
                    label="City"
                    readonly
                  />
                </v-flex>
                <v-flex>
                  <v-text-field
                    hide-details
                    :value="state"
                    color="primary"
                    label="State"
                    readonly
                  />
                </v-flex>
                <v-flex>
                  <v-text-field
                    hide-details
                    :value="country"
                    color="primary"
                    label="Country"
                    readonly
                  />
                </v-flex>
                <v-flex>
                  <v-text-field
                    hide-details
                    :value="postal"
                    color="primary"
                    label="Postal code"
                    readonly
                  />
                </v-flex>
              </v-layout>
            </v-container>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" depressed @click="window = 2">
                Next
              </v-btn>
            </v-card-actions>
          </v-window-item>
          <v-window-item :value="2">
            <v-card-title>Upload box</v-card-title>
            <v-card-text>
              <app-uppy
                ref="uppy"
                :config="{
                  restrictions: {
                    maxNumberOfFiles: 1,
                    allowedFileTypes: ['image/jpeg', 'image/png']
                  }
                }"
              ></app-uppy>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-btn
                :disabled="loading"
                color="primary"
                text
                @click="window = 1"
              >
                back
              </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                :disabled="loading"
                depressed
                @click="initShip"
              >
                ship
              </v-btn>
            </v-card-actions>
          </v-window-item>
          <v-window-item :value="3">
            <v-card>
              <v-flex grow class="pa-4 text-center">
                <v-icon color="success" size="100" v-text="mdiCheckCircle">
                </v-icon>
              </v-flex>
              <v-card-title class="justify-center">
                <span class="text-break text-center">
                  Product marked as shipped
                </span>
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
import { mdiCheckCircle } from "@mdi/js";

import AppLayout from "~/components/Layout/app.vue";
import AppUppy from "~/components/uppy";

import { shipProduct } from "~/assets/js/ship";

export default {
  middleware: "auth",
  data() {
    return {
      name: "Nancy D. Williams",
      address: "2083 René-Lévesque Blvd",
      city: "Montreal",
      state: "QC",
      country: "Canada",
      postal: "H3B 4W8",
      phone: "514-568-3685",
      email: "NancyDWilliams@hotmail.com",
      window: 1,
      loading: false,
      mdiCheckCircle
    };
  },
  methods: {
    goHome() {
      window.history.length > 1 ? this.$router.go(-1) : this.$router.push("/");
    },
    initShip() {
      this.loading = true;

      this.$refs.uppy
        .upload()
        .then(({ successful }) => {
          if (successful.length) return Promise.resolve(true);

          return Promise.resolve(false);
        })
        .then(uploaded => {
          if (uploaded) this.window = 3;

          this.loading = false;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  components: { AppLayout, AppUppy }
};
</script>