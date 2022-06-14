<template>
  <div class="text-center">
    <v-dialog
        v-model="dialog"
        width="700"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn text color="primary"
               v-bind="attrs"
               v-on="on">
          New account
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Create new account
        </v-card-title>

        <v-card-text class="mt-5">
          <v-text-field label="Account name" v-model="name"></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
              color="primary"
              text
              depressed
              @click="saveAccount"
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
  name: "NewAccountDialog",

  data: () => ({
    name: '',

    dialog: false
  }),

  methods: {
    saveAccount() {
      axios.post('/api/v1/admin/ac',
        {
            name: this.name,
          })
          .then((x) => {
            this.dialog = false
            this.emitChange()
          })
    },
    emitChange() {
      this.$emit('data-change')
    }
  }
}
</script>

<style scoped>

</style>