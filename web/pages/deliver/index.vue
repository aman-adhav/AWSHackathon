<template>
  <app-layout title="Deliver">
    <v-container class="pa-4">
      <v-card :loading="loading">
        <v-window touchless v-model="window">
          <v-window-item :value="1">
            <v-card-title class="pb-0">Enter order</v-card-title>
            <v-form @submit="nextStep" ref="orderForm" lazy-validation>
              <v-container class="pa-4" fluid grid-list-md>
                <v-layout>
                  <v-flex>
                    <v-text-field
                      :rules="[rules.required]"
                      color="primary"
                      label="Order ID"
                      v-model="id"
                    ></v-text-field>
                  </v-flex>
                </v-layout>
              </v-container>
              <v-divider></v-divider>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="primary" depressed>
                  next
                </v-btn>
              </v-card-actions>
            </v-form>
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
                text
                color="primary"
                @click="window = 1"
                >back</v-btn
              >
              <v-spacer></v-spacer>
              <v-btn
                :disabled="loading"
                @click="submitDelivery"
                color="primary"
                depressed
                >submit</v-btn
              >
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
                <span class="text-break text-center" v-text="state"></span>
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

import AppLayout from "~/components/Layout/app";
import AppUppy from "~/components/uppy";

export default {
  middleware: "auth/delivery",
  head() {
    this.$store.commit("setPageTitle", "Deliver");

    return {
      title: this.$store.state.pageTitle
    };
  },
  data() {
    return {
      loading: false,
      window: 1,
      id: "",
      rules: {
        required: value => !!value || "Required."
      },
      state: "No Damage Detected",
      damaged: false,
      mdiCheckCircle,
      mdiClose
    };
  },
  methods: {
    goHome() {
      this.window = 1;
      this.id = "";
      this.state = "No Damage Detected";
      this.damaged = false;
      this.$refs.orderForm.resetValidation();
      this.$refs.uppy.uppy.reset();
    },
    nextStep(event) {
      event.preventDefault();

      if (this.$refs.orderForm.validate()) this.window = 2;
    },
    submitDelivery() {
      this.loading = true;

      this.$refs.uppy.uppy.getPlugin(
        "XHRUpload"
      ).opts.endpoint = `http://localhost:5002/upload_to_check_damage/${this.id}`;

      this.$refs.uppy
        .upload()
        .then(({ successful, failed }) => {
          if (!successful.length || failed.length)
            return Promise.resolve(false);

          for (let i = 0; i < successful.length; i++) {
            const { body } = successful[i].response;

            if (body.damaged) {
              this.damaged = true;
              this.state = body.state;
              return Promise.resolve(true);
            }
          }

          return Promise.resolve(true);
        })
        .then(uploaded => {
          if (!uploaded) return;

          this.window = 3;

          this.loading = false;
        });
    }
  },
  components: { AppLayout, AppUppy }
};
</script>