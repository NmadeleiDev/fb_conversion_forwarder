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
          Add BM
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Add new BM record
        </v-card-title>

        <v-card-text class="mt-5">
          <v-card-subtitle>BM settings</v-card-subtitle>
          <v-text-field label="Local BM name" v-model="name"></v-text-field>
          <v-text-field label="Business manager access token" v-model="accessToken"></v-text-field>
          <v-text-field label="Facebook pixel ID" v-model="pixelId"></v-text-field>
          <v-text-field label="Test event code" v-model="testEventCode"></v-text-field>

          <v-select label="Event source domain" :items="domains.map(x => x.domain)" v-model="eventsourceDomain"></v-select>

          <v-select label="Facebook event name" :items="fbEventNames" v-model="fbEventName"></v-select>

          <v-card-subtitle>Fields to send to Facebook API</v-card-subtitle>
          <div class="d-flex flex-row flex-wrap">
            <v-checkbox dense class="mr-5" v-for="field in userDataFieldsConst" :key="field"
                        v-model="userDataFields" :label="field" :value="field"></v-checkbox>
          </div>

          <v-card-subtitle class="mt-3">Fields to random generate if not present</v-card-subtitle>
          <div class="d-flex flex-row flex-wrap">
            <v-checkbox dense class="mr-5" v-for="field in fakeableDataFieldsConst" :key="field"
                        v-model="fakeableDataFields" :label="field" :value="field"></v-checkbox>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
              color="primary"
              text
              depressed
              @click="saveBm"
          >
            Add
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
  name: "NewBmDialog",

  props: {
    acid: String,
    userDataFieldsConst: Array,
    fakeableDataFieldsConst: Array,
    domains: Array
  },

  data: () => ({
    name: '',
    accessToken: '',
    pixelId: '',
    testEventCode: '',
    eventsourceDomain: '',
    userDataFields: [],
    fakeableDataFields: [],
    fbEventName: 'Lead',

    dialog: false,

    fbEventNames: [
      'Lead',
      'PageView',
      'CompleteRegistration',
      'Purchase',
      'Search',
      'ViewContent'
    ]
  }),

  methods: {
    saveBm() {
      axios.post(`/api/v1/admin/bm?test_code=${this.testEventCode}`,
        {
            name: this.name,
            ad_container_id: this.acid,
            access_token: this.accessToken,
            pixel_id: this.pixelId,
            fields_sent: this.userDataFields,
            fields_generated: this.fakeableDataFields,
            event_source_domain: this.eventsourceDomain,
            fb_event_name: this.fbEventName,
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