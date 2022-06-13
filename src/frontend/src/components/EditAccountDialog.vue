<template>
  <div class="text-center">
    <v-dialog
        v-model="dialog"
        width="700"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn text color="primary" v-bind="attrs"
               v-on="on">
          <v-icon
              >mdi-cog-outline</v-icon>
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Edit account '{{bm.name}}'
        </v-card-title>

        <v-card-text class="mt-5">
          <v-text-field label="Account name" v-model="bm.name"></v-text-field>
          <v-text-field label="Business manager access token" v-model="bm.access_token"></v-text-field>
          <v-text-field label="Facebook pixel ID" v-model="bm.pixel_id"></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
              color="primary"
              text
              @click="saveAccount"
          >
            Save
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
  name: "EditAccountDialog",

  props: {
    bm: Object
  },

  data: () => ({
    dialog: false
  }),

  methods: {
    saveAccount() {
      axios.put('/api/v1/admin/bm',
          {
            id: this.bm.id,
            name: this.bm.name,
            access_token: this.bm.access_token,
            pixel_id: this.bm.pixel_id,
          }).then((x) => {
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