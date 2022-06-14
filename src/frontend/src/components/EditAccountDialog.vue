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
          Edit account '{{account.name}}'
        </v-card-title>

        <v-card-text class="mt-5">
          <div class="d-flex flex-row flex-fill">
            <v-text-field label="Account name" v-model="account.name"></v-text-field>

            <v-btn
                color="primary"
                text
                @click="saveAccount"
            >
              Save
            </v-btn>
          </div>

          <div class="d-flex flex-column">
            <h3 class="mb-3 ma-6">Account BMs</h3>
            <div class="d-flex flex-row flex-fill">
              <v-text-field v-if="bms.length > 0"
                  label="Filter BMs"
                  v-model="bmSearchStr"
                  class="mr-7"
              >
              </v-text-field>
              <NewBmDialog v-on:data-change="emitChange" :acid="account.id"></NewBmDialog>
            </div>
          </div>

          <v-list three-line>
            <v-list-item v-for="bm in filteredBms" :key="bm.id">
              <v-list-item-content>
                <v-list-item-title>
                  {{bm.name}}
                </v-list-item-title>
                <v-list-item-subtitle>Access token: {{bm.access_token}}</v-list-item-subtitle>
                <v-list-item-subtitle>Pixel id: {{bm.pixel_id}}</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <EditBmDialog v-on:data-change="emitChange" :bm="bm"></EditBmDialog>
                <DeleteBmDialog v-on:data-change="emitChange" :bm="bm"></DeleteBmDialog>
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
import EditBmDialog from "@/components/EditBmDialog";
import DeleteBmDialog from "@/components/DeleteBmDialog";
import NewBmDialog from "@/components/NewBmDialog";

export default {
  name: "EditAccountDialog",
  components: {NewBmDialog, EditBmDialog, DeleteBmDialog},
  props: {
    account: Object
  },

  data: () => ({
    bms: [],
    bmSearchStr: '',
    dialog: false
  }),

  created() {
    this.loadBms()
  },

  methods: {
    loadBms() {
      axios.get(`/api/v1/admin/bm?ac_id=${this.account.id}`).then((resp) => {
        while (this.bms.length) {this.bms.pop()}
        resp.data.forEach(x => this.bms.push(x))
      })
    },

    saveAccount() {
      axios.put('/api/v1/admin/ac',
          {
            id: this.account.id,
            name: this.account.name,
          }).then((x) => {
        this.dialog = false
        this.emitChange()
      })
    },
    emitChange() {
      this.$emit('data-change')
    }
  },
  computed: {
    filteredBms() {
      if (this.bmSearchStr) {
        return this.bms.filter(
            x => x.name.toString().includes(this.bmSearchStr) || x.id.toString().includes(this.bmSearchStr))
      } else {
        return this.bms
      }
    }
  }
}
</script>

<style scoped>

</style>