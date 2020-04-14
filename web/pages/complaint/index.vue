<template>
  <app-layout title="Complaints">
    <v-container class="pa-4">
      <v-card>
        <v-window touchless v-model="window">
          <v-window-item :value="1">
            <v-card-title class="pb-0">Enter order</v-card-title>
            <v-form @submit="nextStep" ref="orderForm" lazy-validation>
              <v-container class="pa-4" fluid grid-list-md>
                <v-layout wrap>
                  <v-flex xs12>
                    <v-text-field
                      :rules="[rules.required]"
                      color="primary"
                      label="Order ID"
                    ></v-text-field>
                  </v-flex>
                  <v-flex xs12>
                    <v-textarea
                      :rules="[rules.required]"
                      color="primary"
                      label="Complaint details"
                    ></v-textarea>
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
          </v-window-item>
        </v-window>
      </v-card>
    </v-container>
  </app-layout>
</template>

<script>
import AppLayout from "~/components/Layout/app";
import AppUppy from "~/components/uppy";

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
      window: 1,
      rules: {
        required: value => !!value || "Required."
      }
    };
  },
  methods: {
    nextStep(event) {
      event.preventDefault();

      if (this.$refs.orderForm.validate()) this.window = 2;
    }
  },
  components: { AppLayout, AppUppy }
};
</script>