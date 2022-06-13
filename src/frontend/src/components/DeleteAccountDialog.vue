<template>
  <div class="text-center">
    <v-dialog
        v-model="dialog"
        width="700"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn text color="error" v-bind="attrs"
               v-on="on">
          <v-icon
              >mdi-delete</v-icon>
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Delete account '{{bm.name}}'
        </v-card-title>

        <v-card-text class="mt-5">
          Are you sure that you want to delete account '{{bm.name}}'?
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
              color="error"
              text
              @click="deleteAccount"
          >
            Delete account
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
  name: "DeleteAccountDialog",

  props: {
    bm: Object
  },

  data: () => ({
    dialog: false
  }),

  methods: {
    deleteAccount() {
      axios.delete(`/api/v1/admin/bm?bm_id=${this.bm.id}`).then((x) => {
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