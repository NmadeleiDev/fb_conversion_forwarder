<template>
  <div class="text-center">
    <v-dialog
        v-model="dialog"
        width="700"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn text v-bind="attrs"
               v-on="on">
        <v-icon color="grey lighten-1"
                  >mdi-information</v-icon>
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Account {{account.name}}
        </v-card-title>

        <v-card-text class="mt-5">
          Here is forwarder pixel for account '{{account.name}}'. Give it to the advertiser to add to the website.
        </v-card-text>

        <v-textarea :value="pixel" class="ma-4" label="Account pixel">
        </v-textarea>

        <v-divider></v-divider>

        <v-card-actions>
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
  name: "AccountInfoDialog",

  props: {
    account: Object
  },

  data: () => ({
    pixel: '',
    dialog: false
  }),

  created() {
    axios.get(`/api/v1/admin/pixel?ac_id=${this.account.id}`).then(resp => {
      this.pixel = resp.data
    })
  },
}
</script>

<style scoped>

</style>