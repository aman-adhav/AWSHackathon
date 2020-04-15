<template>
  <app-layout title="Orders" :loading="loading">
    <v-container grid-list-md>
      <v-layout wrap>
        <template v-for="(stat, i) in stats">
          <v-flex :key="i">
            <v-card>
              <v-container fluid>
                <v-layout align-center>
                  <v-flex shrink>
                    <v-avatar>
                      <v-icon v-text="stat.icon"></v-icon>
                    </v-avatar>
                  </v-flex>
                  <v-flex grow>
                    <v-layout column>
                      <v-flex class="text-right">
                        <span class="title" v-text="stat.value"></span>
                      </v-flex>
                      <v-flex class="text-right">
                        <span
                          class="font-weight-light"
                          v-text="stat.title"
                        ></span>
                      </v-flex>
                    </v-layout>
                  </v-flex>
                </v-layout>
              </v-container>
            </v-card>
          </v-flex>
        </template>
      </v-layout>
      <v-layout>
        <v-flex>
          <v-card>
            <v-data-table
              :headers="headers"
              :items="orders"
              item-key="product_id"
            >
              <template v-slot:item.image="{ item }">
                <template v-if="item.images.length">
                  <div class="order-image-container py-2">
                    <img height="64" width="auto" :src="item.images[0]" />
                  </div>
                </template>
                <template v-else>
                  <v-icon x-large v-text="mdiPackageVariantClosed"></v-icon>
                </template>
              </template>
              <template v-slot:item.date="{ item }">
                {{ item.date.toLocaleString() }}
              </template>
              <template v-slot:item.payment="{ item }">
                <v-chip
                  :class="
                    item.payment === 'paid' ? 'chip-green' : 'chip-orange'
                  "
                  >{{ item.payment }}</v-chip
                >
              </template>
              <template v-slot:item.status="{ item }">
                <v-chip
                  :class="{
                    'chip-green': item.status === 'completed',
                    'chip-orange': item.status === 'shipped'
                  }"
                  >{{ item.status }}</v-chip
                >
              </template>
              <template v-slot:item.total="{ item }">
                <span v-text="formatCurrency(item.total)"></span>
              </template>
              <template v-slot:item.actions="{ item }">
                <v-menu left offset-y>
                  <template v-slot:activator="{ on }">
                    <v-btn icon v-on="on">
                      <v-icon v-text="mdiDotsVertical"></v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item :disabled="item.status !== 'unfulfilled'" :to="`/orders/${item.product_id}/ship`">
                      <v-list-item-title>Ship</v-list-item-title>
                    </v-list-item>
                    <!-- <v-list-item @click="() => true">
                      <v-list-item-title>Delete</v-list-item-title>
                    </v-list-item> -->
                  </v-list>
                </v-menu>
              </template>
            </v-data-table>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </app-layout>
</template>

<style lang="scss">
$chip-opacity: 0.8;

.chip-green {
  background-color: change-color(
    map-get($green, "base"),
    $alpha: $chip-opacity
  ) !important;
}

.chip-orange {
  background-color: change-color(
    map-get($orange, "base"),
    $alpha: $chip-opacity
  ) !important;
}
</style>

<script>
import AppLayout from "~/components/Layout/app.vue";

import {
  mdiFinance,
  mdiPackageVariantClosed,
  mdiReceipt,
  mdiAccountMultiple,
  mdiDotsVertical
} from "@mdi/js";

export default {
  middleware: "auth/vendor",
  head() {
    this.$store.commit("setPageTitle", "Orders");

    return {
      title: this.$store.state.pageTitle
    };
  },
  data() {
    this.formatter = new Intl.NumberFormat(undefined, {
      style: "currency",
      currency: "USD"
    });

    return {
      loading: true,
      mdiDotsVertical,
      stats: [
        {
          title: "Average order value",
          value: "$18.54",
          icon: mdiFinance
        },
        {
          title: "Total orders",
          value: 4,
          icon: mdiPackageVariantClosed
        },
        {
          title: "Total sales",
          value: "$81.10",
          icon: mdiReceipt
        },
        {
          title: "Total visitors",
          value: 32,
          icon: mdiAccountMultiple
        }
      ],
      headers: [
        {
          text: "Image",
          value: "image",
          sortable: false,
          align: "center"
        },
        {
          text: "Product",
          value: "product_name"
        },
        { text: "Status", value: "status", align: "center" },
        { text: "Actions", value: "actions", align: "center", sortable: false }
      ],
      orders: [],
      mdiPackageVariantClosed
    };
  },
  mounted() {
    this.fetchItems();
  },
  methods: {
    formatCurrency(number) {
      return this.formatter.format(number);
    },
    fetchItems() {
      this.$axios({
        method: "POST",
        url: "http://localhost:5000/get_item_list"
      })
        .then(({ data }) => {
          if (data.list_items) this.orders = data.list_items;
          else this.orders = [];
        })
        .catch(error => {
          console.error(error);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  components: { AppLayout }
};
</script>