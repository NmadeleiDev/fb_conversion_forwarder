<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <h2>FB Conversions Forwarder</h2>
      </div>

      <v-spacer></v-spacer>
      <LoginDialog></LoginDialog>
      <CreateAccDialog v-if="isLogged"></CreateAccDialog>
    </v-app-bar>

    <v-main>
      <v-container>
        <v-card v-if="isLogged">
          <v-card-title>
            Accounts
            <v-spacer></v-spacer>
            <NewAccountDialog v-on:data-change="reloadData"></NewAccountDialog>
          </v-card-title>
          <v-text-field
              filled
              label="Filter accounts"
              v-model="bmSearchStr"
              class="mr-7 ml-7"
          >
          </v-text-field>
          <v-list rounded>
            <BmItem v-on:data-change="reloadData" v-for="bm in filteredBms" :bm="bm" :key="bm.id"></BmItem>
          </v-list>
        </v-card>
        <LoginDialog v-else></LoginDialog>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Vue from 'vue';
import BmItem from './components/BmItem.vue';
import axios from "axios";
import NewAccountDialog from "@/components/NewAccountDialog";
import LoginDialog from "@/components/LoginDialog";
import CreateAccDialog from "@/components/CreateAccDialog";

export default Vue.extend({
  name: 'App',

  components: {
    CreateAccDialog,
    LoginDialog,
    NewAccountDialog,
    BmItem,
  },

  data: () => ({
    bms: [],
    bmSearchStr: '',

    isLogged: false
  }),

  created() {
    this.checkIsLogged()
    this.reloadData()
  },

  methods: {
    reloadData() {
      while (this.bms.length) {this.bms.pop()}
      axios.get("/api/v1/admin/bm").then(resp => {
        resp.data.forEach(x => this.bms.push(x))
      })
    },

    checkIsLogged() {
      axios.get("/api/v1/admin/account").then(resp => {
        this.isLogged = true
      }).catch((x) => {
        this.isLogged = false
      })
    },
  },
  computed: {
    filteredBms() {
      if (this.bmSearchStr) {
        return this.bms.filter(
            x => x.name.toString().includes(this.bmSearchStr) || x.id.toString().includes(this.bmSearchStr))
      } else {
        return this.bms
      }
    }
  }
});
</script>
