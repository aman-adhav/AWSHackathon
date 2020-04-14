<template>
  <app-layout title="Orders">
    <!-- <v-btn @click="test">test</v-btn> -->
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
            <v-data-table :headers="headers" :items="orders" item-key="id">
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
                    <v-list-item
                      :disabled="item.payment !== 'paid'"
                      :to="`/orders/${item.id}/ship`"
                    >
                      <v-list-item-title>Ship</v-list-item-title>
                    </v-list-item>
                    <v-list-item @click="() => true">
                      <v-list-item-title>Delete</v-list-item-title>
                    </v-list-item>
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
          text: "Product",
          value: "product.name"
        },
        { text: "Date", value: "date" },
        { text: "Quantity", value: "quantity", align: "center" },
        { text: "Payment", value: "payment", align: "center" },
        { text: "Status", value: "status", align: "center" },
        { text: "Total", value: "total" },
        { text: "Actions", value: "actions", align: "center", sortable: false }
      ],
      orders: [
        {
          id: "5e87975045682e9ceff61ac4",
          quantity: 7,
          date: new Date("Tue Mar 10 2020 06:29:13 GMT+0000 (UTC)"),
          payment: "pending",
          total: 94.21,
          status: "unfulfilled",
          product: {
            id: "5e87975078b04f2289ba25f7",
            name: "Leggings",
            image: "/sample_leggings_product.jpeg"
          }
        },
        {
          id: "5e879750970028a18cc3045d",
          quantity: 9,
          date: new Date("Fri Feb 14 2020 16:53:00 GMT+0000 (UTC)"),
          payment: "paid",
          total: 196.48,
          status: "unfulfilled",
          product: {
            id: "5e879750f345db849675ece6",
            name: "Leggings",
            image: "/sample_leggings_product.jpeg"
          }
        },
        {
          id: "5e87975056262ec1bf954779",
          quantity: 5,
          date: new Date("Fri Feb 14 2020 06:20:13 GMT+0000 (UTC)"),
          payment: "pending",
          total: 67.15,
          status: "unfulfilled",
          product: {
            id: "5e879750a60436750b87c50a",
            name: "Leggings",
            image: "/sample_leggings_product.jpeg"
          }
        },
        {
          id: "5e8797506fcd0113861c13f7",
          quantity: 5,
          date: new Date("Mon Feb 03 2020 07:25:53 GMT+0000 (UTC)"),
          payment: "paid",
          total: 26.4,
          status: "unfulfilled",
          product: {
            id: "5e879750d6c3655037256d73",
            name: "Leggings",
            image: "/sample_leggings_product.jpeg"
          }
        },
        {
          id: "5e8797501e694815e51b77b5",
          quantity: 1,
          date: new Date("Fri Feb 28 2020 10:09:38 GMT+0000 (UTC)"),
          payment: "paid",
          total: 155.47,
          status: "unfulfilled",
          product: {
            id: "5e8797503bedf858a90bb018",
            name: "Leggings",
            image: "/sample_leggings_product.jpeg"
          }
        },
        {
          id: "5e8797505f477087e79f0483",
          quantity: 3,
          date: new Date("Sun Jan 26 2020 11:09:55 GMT+0000 (UTC)"),
          payment: "paid",
          total: 99.53,
          status: "unfulfilled",
          product: {
            id: "5e8797501e9f15d7dc7a8e74",
            name: "Leggings",
            image: "/sample_leggings_product.jpeg"
          }
        }
      ]
    };
  },
  methods: {
    formatCurrency(number) {
      return this.formatter.format(number);
    },
    test() {
      this.$axios({
        method: "GET",
        url: "http://localhost:5000/api/private",
        headers: { Authorization: `Bearer ${this.$auth.accessToken}` }
      })
        .then(({ data }) => {
          console.log(data);
        })
        .catch(error => console.error(error));
    }
  },
  components: { AppLayout }
};
</script>