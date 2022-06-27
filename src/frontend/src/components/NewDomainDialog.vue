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
          Add Domain
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          Add new Domain for FB auth
        </v-card-title>

        <v-card-text class="mt-5">
          <v-card-subtitle>Domain settings</v-card-subtitle>
          <v-text-field label="Domain string" placeholder="example.com" v-model="domain"></v-text-field>
          <v-text-field label="Facebook Meta Tag" v-model="fbMetaTag"></v-text-field>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
              color="primary"
              text
              depressed
              @click="saveDomain"
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
  name: "NewDomainDialog",

  data: () => ({
    dialog: false,

    domain: '',
    fbMetaTag: ''
  }),

  methods: {
    saveDomain() {
      axios.post(`/api/v1/admin/domain`, {
        domain: this.domain,
        fb_meta_tag: this.fbMetaTag
      }).then((res) => {
        console.log("res: ", res)
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