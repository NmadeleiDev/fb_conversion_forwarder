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
          Edit BM '{{bm.name}}'
        </v-card-title>

        <v-card-text class="mt-5">
          <v-card-subtitle>BM settings</v-card-subtitle>
          <v-text-field label="Account name" v-model="bm.name"></v-text-field>
          <v-text-field label="Business manager access token" v-model="bm.access_token"></v-text-field>
          <v-text-field label="Facebook pixel ID" v-model="bm.pixel_id"></v-text-field>

          <v-select label="Event source domain" :items="domains.map(x => x.domain)" v-model="bm.event_source_domain"></v-select>

          <v-select label="Facebook event name" :items="fbEventNames" v-model="bm.fb_event_name"></v-select>

          <v-card-subtitle>Fields to send to Facebook API</v-card-subtitle>
          <div class="d-flex flex-row flex-wrap">
          <v-checkbox class="ml-5" v-for="field in userDataFieldsConst" :key="field"
                      v-model="bm.fields_sent" :label="field" :value="field"></v-checkbox>
          </div>

          <v-card-subtitle class="mt-3">Fields to random generate if not present</v-card-subtitle>
          <div class="d-flex flex-row flex-wrap">
            <v-checkbox class="ml-5" v-for="field in fakeableDataFieldsConst" :key="field"
                        v-model="bm.fields_generated" :label="field" :value="field"></v-checkbox>
          </div>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
              color="primary"
              text
              @click="saveBm"
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
  name: "EditBmDialog",

  props: {
    bm: Object,
    userDataFieldsConst: Array,
    fakeableDataFieldsConst: Array,
    domains: Array
  },

  data: () => ({
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
      axios.put('/api/v1/admin/bm',
          {
            id: parseInt(this.bm.id),
            ad_container_id: parseInt(this.bm.ad_container_id),
            name: this.bm.name,
            access_token: this.bm.access_token,
            pixel_id: this.bm.pixel_id,
            fields_sent: this.bm.fields_sent,
            fields_generated: this.bm.fields_generated,
            event_source_domain: this.bm.event_source_domain,
            fb_event_name: this.bm.fb_event_name
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