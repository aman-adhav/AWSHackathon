<template>
  <app-layout title="Complaints">
    <v-container class="pa-4">
      <v-card :loading="loading" :disabled="loading">
        <v-window touchless v-model="window">
          <v-window-item :value="1">
            <v-card-title class="pb-0">Enter order</v-card-title>
            <v-form @submit="nextStep" ref="orderForm" lazy-validation>
              <v-container class="pa-4" fluid grid-list-md>
                <v-layout wrap>
                  <v-flex xs12>
                    <v-text-field
                      v-model="id"
                      :rules="[rules.required]"
                      color="primary"
                      label="Order ID"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-textarea
                      v-model="complaint"
                      :rules="[rules.required]"
                      color="primary"
                      label="Complaint details"
                    ></v-textarea>
                  </v-flex>
                </v-layout>
                <v-layout wrap>
                  <v-flex shrink>
                    <v-checkbox
                      hide-details="auto"
                      color="primary"
                      label="Was the product fake?"
                      type="checkbox"
                      v-model="productFake"
                    ></v-checkbox>
                  </v-flex>
                  <v-flex shrink>
                    <v-checkbox
                      hide-details="auto"
                      color="primary"
                      label="Was the product damaged?"
                      type="checkbox"
                      v-model="productDamaged"
                    ></v-checkbox>
                  </v-flex>
                  <v-flex shrink>
                    <v-checkbox
                      hide-details="auto"
                      color="primary"
                      label="Was the box damaged?"
                      type="checkbox"
                      v-model="boxDamaged"
                    ></v-checkbox>
                  </v-flex>
                </v-layout>
              </v-container>
              <v-divider></v-divider>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="primary" depressed>
                  submit
                </v-btn>
              </v-card-actions>
            </v-form>
          </v-window-item>
          <v-window-item :value="2">
            <v-card>
              <v-flex grow class="pa-4 text-center">
                <v-icon color="success" size="100" v-text="mdiCheckCircle">
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
          <!-- <v-window-item :value="2">
            <v-card-title>Upload box</v-card-title>
            <v-card-text>
              <app-uppy
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
              <v-btn text color="primary" @click="window = 1">back</v-btn>
              <v-spacer></v-spacer>
              <v-btn color="primary" depressed>submit</v-btn>
            </v-card-actions>
          </v-window-item> -->
        </v-window>
      </v-card>
    </v-container>
  </app-layout>
</template>

<script>
import AppLayout from "~/components/Layout/app";
import AppUppy from "~/components/uppy";

import { mdiCheckCircle } from "@mdi/js";

export default {
  middleware: "auth/customer",
  head() {
    this.$store.commit("setPageTitle", "Complaints");

    return {
      title: this.$store.state.pageTitle
    };
  },
  data() {
    return {
      id: "",
      complaint: "",
      productFake: false,
      productDamaged: false,
      boxDamaged: false,
      window: 1,
      loading: false,
      message: "",
      mdiCheckCircle,
      rules: {
        required: value => !!value || "Required."
      }
    };
  },
  methods: {
    nextStep(event) {
      event.preventDefault();

      if (this.$refs.orderForm.validate()) this.sendComplaint();

      // if (this.$refs.orderForm.validate()) this.window = 2;
    },
    goHome() {
      this.$refs.orderForm.resetValidation();
      this.id = "";
      this.complaint = "";
      this.productFake = false;
      this.productDamaged = false;
      this.boxDamaged = false;
      this.window = 1;
    },
    sendComplaint() {
      this.loading = true;

      const complaint = {
        description: this.complaint,
        box_damaged: this.boxDamaged,
        product_fake: this.productFake,
        product_damaged: this.productDamaged
      };

      return this.$axios({
        method: "POST",
        url: `http://localhost:5003/send_complaint/${this.id}`,
        data: complaint
      })
        .then(({ data }) => {
          return this.$axios({
            method: "POST",
            url: `http://localhost:5003/review_complaint/${this.id}`
          });
        })
        .then(({ data }) => {
          this.loading = false;
          this.window = 2;

          this.message = data.message;
        });
    }
  },
  components: { AppLayout, AppUppy }
};
</script>