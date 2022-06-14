<template>
  <div class="text-center">
    <v-dialog
        v-model="dialog"
        width="700"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            text
            v-bind="attrs"
            v-on="on">
          <span class="mr-2">Create account</span>
          <v-icon>mdi-account-plus</v-icon>
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Create New Account
        </v-card-title>

        <v-card-text class="mt-5">
          <v-text-field label="Email" v-model="email"></v-text-field>
          <v-text-field label="Password" v-model="password"></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
              color="primary"
              text
              depressed
              @click="sendCreateReq"
          >
            Create
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
              color="secondary"
              text
              @click="dialog = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CreateAccDialog",

  data: () => ({
    email: '',
    password: '',

    dialog: false
  }),

  methods: {
    sendCreateReq() {
      axios.post('/api/v1/admin/account',
          {
            email: this.email,
            password: this.password,
          })
          .then((x) => {
            this.dialog = false
          }).catch(x => console.log(x))
    }
  }
}
</script>

<style scoped>

</style>