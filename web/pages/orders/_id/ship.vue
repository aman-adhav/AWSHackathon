<template>
  <app-layout title="Ship order">
    <v-container class="pa-4">
      <v-card :loading="loading">
        <v-window touchless v-model="window">
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
              <v-btn color="primary" depressed @click="nextStep">
                Next
              </v-btn>
            </v-card-actions>
          </v-window-item>
          <v-window-item :value="2">
            <v-card-title>Upload box</v-card-title>
            <v-card-text>
              <app-uppy ref="uppy"></app-uppy>
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
                <v-icon
                  v-if="!damaged"
                  color="success"
                  size="100"
                  v-text="mdiCheckCircle"
                >
                </v-icon>
                <v-icon v-else color="error" size="100" v-text="mdiClose">
                </v-icon>
              </v-flex>
              <v-card-title class="justify-center">
                <span v-if="!damaged" class="text-break text-center">
                  Product marked as shipped
                </span>
                <span v-else class="text-break text-center">
                  We believe this product has been damaged. Try again.
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
import { mdiCheckCircle, mdiClose } from "@mdi/js";

import AppLayout from "~/components/Layout/app.vue";
import AppUppy from "~/components/uppy";

import { shipProduct } from "~/assets/js/ship";

export default {
  middleware: "auth/vendor",
  head() {
    this.$store.commit("setPageTitle", "Ship product");

    return {
      title: this.$store.state.pageTitle
    };
  },
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
      uploaded: false,
      damaged: false,
      mdiCheckCircle,
      mdiClose
    };
  },
  methods: {
    nextStep() {
      this.window = 2;
    },
    goHome() {
      window.history.length > 1 ? this.$router.go(-1) : this.$router.push("/");
    },
    initShip() {
      this.loading = true;

      const { id } = this.$route.params;

      if (this.uploaded) {
        this.checkForDamage(id);
        return;
      }

      this.$refs.uppy.uppy.getPlugin(
        "XHRUpload"
      ).opts.endpoint = `http://localhost:5001/upload_for_shipment/${id}`;

      this.$refs.uppy
        .upload()
        .then(({ successful, failed }) => {
          if (!successful.length || failed.length)
            return Promise.resolve(false);

          return Promise.resolve(true);
        })
        .then(uploaded => {
          this.uploaded = uploaded;

          if (uploaded) return this.checkForDamage(id);
        })
        .catch(error => {
          console.error(error);
        });
    },
    checkForDamage(id) {
      return this.$axios({
        method: "POST",
        url: `http://localhost:5001/check_for_damage/${id}`
      })
        .then(({ data }) => {
          if (data.damaged === false) this.damaged = false;
          else this.damaged = true;

          if (!this.damaged) return this.shipItem(id);
          return Promise.resolve();
        })
        .then(() => {
          this.loading = false;

          this.window = 3;
        });
    },
    shipItem(id) {
      return this.$axios({
        method: "GET",
        url: `http://localhost:5001/ship_item/${id}`
      });
    }
  },
  components: { AppLayout, AppUppy }
};
</script>