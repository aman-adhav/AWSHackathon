<template>
  <v-container fluid fill-height>
    <v-layout fill-height align-center justify-center>
      <v-flex shrink>
        <v-card max-width="500">
          <v-card-title class="headline primary white--text"
            >Login</v-card-title
          >
          <v-form>
            <v-container fluid grid-list-md>
              <v-layout wrap>
                <v-flex xs12>
                  <v-text-field
                    :prepend-icon="mdiAccount"
                    label="Username"
                  ></v-text-field>
                </v-flex>
                <v-flex xs12>
                  <v-text-field
                    :prepend-icon="mdiLock"
                    label="Password"
                  ></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
          </v-form>
          <v-card-actions right>
            <v-spacer></v-spacer>
            <v-btn @click="$store.commit('login')" color="primary">Login</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import { mdiAccount, mdiLock } from "@mdi/js";

export default {
  data() {
    return { mdiAccount, mdiLock };
  }
};
</script>