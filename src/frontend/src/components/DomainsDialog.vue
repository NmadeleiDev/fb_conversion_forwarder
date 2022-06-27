<template>
  <div class="text-center">
    <v-dialog
        v-model="dialog"
        width="700"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn text color="primary"
               v-bind="attrs"
               v-on="on"> Domains
        </v-btn>
      </template>

      <v-card>
        <v-card-title class="text-h5 grey lighten-2">
          FB authorized domains
        </v-card-title>

        <v-card-text class="mt-5">

          <NewDomainDialog v-on:data-change="emitChange"></NewDomainDialog>
          <v-list two-line>
            <v-list-item v-for="domain in domains" :key="domain.id">
              <v-list-item-content>
                <v-list-item-title>
                  {{domain.domain}}
                </v-list-item-title>
                <v-list-item-subtitle>Meta tag: {{domain.fb_meta_tag}}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn text color="error" @click="sendDeleteDomainReq(domain.id)">
                  <v-icon
                      >mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card-text>

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
import NewDomainDialog from "@/components/NewDomainDialog";

export default {
  name: "DomainsDialog",
  components: {NewDomainDialog},
  props: {
    domains: Array
  },

  data: () => ({
    dialog: false
  }),

  methods: {
    sendDeleteDomainReq(domainId) {
      axios.delete(`/api/v1/admin/domain?id=${domainId}`).then((res) => {
        console.log('deleted')
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