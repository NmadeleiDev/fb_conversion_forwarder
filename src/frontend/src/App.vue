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
      <CreateSystemAccountDialog v-if="isLogged"></CreateSystemAccountDialog>
    </v-app-bar>

    <v-main>
      <v-container>
        <ServiceAlert :content="alertText" :val="showAlert"></ServiceAlert>
        <v-card v-if="isLogged">
          <v-card-title>
            Accounts
            <v-spacer></v-spacer>
            <NewAccountDialog v-on:data-change="reloadData"></NewAccountDialog>
          </v-card-title>
          <v-text-field
              filled
              label="Filter accounts"
              v-model="accSearchStr"
              class="mr-7 ml-7"
          >
          </v-text-field>
          <v-list rounded>
            <AccountItem v-on:data-change="reloadData" v-for="ac in filteredAccounts" :account="ac" :key="ac.id"></AccountItem>
          </v-list>
        </v-card>
        <LoginDialog v-else></LoginDialog>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Vue from 'vue';
import axios from "axios";
import NewAccountDialog from "@/components/NewAccountDialog";
import LoginDialog from "@/components/LoginDialog";
import CreateSystemAccountDialog from "@/components/CreateSystemAccountDialog";
import AccountItem from "@/components/AccountItem";
import ServiceAlert from "@/components/ServiceAlert";

export default Vue.extend({
  name: 'App',

  components: {
    ServiceAlert,
    AccountItem,
    CreateSystemAccountDialog,
    LoginDialog,
    NewAccountDialog,
  },

  data: () => ({
    accounts: [],
    accSearchStr: '',

    isLogged: false,

    showAlert: false,
    alertText: ''
  }),

  created() {
    this.checkIsLogged()
    this.reloadData()

    axios.interceptors.response.use(resp => resp, (err) => {
      this.showAlert = true
      this.alertText = err.response.data.msg
      console.log('err handled: ', err)
      this.setTimeoutForAlert()
    });
  },

  methods: {
    setTimeoutForAlert() {
      setTimeout(() => this.showAlert = false, 1000 * 5)
    },
    reloadData() {
      while (this.accounts.length) {this.accounts.pop()}
      axios.get("/api/v1/admin/ac").then(resp => {
        resp.data.forEach(x => this.accounts.push(x))
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
    filteredAccounts() {
      if (this.accSearchStr) {
        return this.accounts.filter(
            x => x.name.toString().includes(this.accSearchStr) || x.id.toString().includes(this.accSearchStr))
      } else {
        return this.accounts
      }
    }
  }
});
</script>
