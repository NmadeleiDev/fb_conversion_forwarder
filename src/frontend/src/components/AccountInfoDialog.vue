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
          Account '{{account.name}}'
        </v-card-title>

        <v-card-text class="mt-5">
          Integration code variants for account '{{account.name}}'. Give it to the advertiser to add to the website.
        </v-card-text>

        <v-tabs
            v-model="integrationVariant"
            background-color="transparent"
            color="basil"
            grow
        >
          <v-tab
              v-for="name in integrationVariants"
              :key="name"
          >
            {{ nameForintegrationVariant(name) }}
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="integrationVariant">
          <v-tab-item
              v-for="name in integrationVariants"
              :key="name"
          >
            <v-card
                color="basil"
                flat
            >
              <v-card-text>{{valForintegrationVariant(name)}}</v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>

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
    dialog: false,

    integrationVariants: ['pixel', 'http_callback_hashed', 'http_callback_raw'],
    integrationVariant: null
  }),

  created() {
    axios.get(`/api/v1/admin/pixel?ac_id=${this.account.id}`).then(resp => {
      this.pixel = resp.data
    })
  },

  methods: {
    nameForintegrationVariant(name) {
      if (name === 'pixel') {
        return 'JS-pixel'
      } else if (name === 'http_callback_hashed') {
        return 'Hashed data http callback'
      } else if (name === 'http_callback_raw') {
        return 'Raw data http callback'
      } else {
        console.log('unknown var:', name)
        return ''
      }
    },
    valForintegrationVariant(name) {
      if (name === 'pixel') {
        return this.pixel
      } else if (name === 'http_callback_hashed') {
        return `https://conversion-router.tech/api/v1/fw/cb/${this.account.id}/${this.account.forwarder_secret}/hashed`
      } else if (name === 'http_callback_raw') {
        return `https://conversion-router.tech/api/v1/fw/cb/${this.account.id}/${this.account.forwarder_secret}/raw`
      } else {
        console.log('unknown var:', name)
        return null
      }
    }
  }
}
</script>

<style scoped>

</style>