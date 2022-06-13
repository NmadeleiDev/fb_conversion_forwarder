<template>
  <v-list-item two-line>
    <v-list-item-content>
      <v-list-item-title class="v-size--large mb-3">{{bm.name}}</v-list-item-title>
      <v-list-item-subtitle>Id: {{bm.id}}</v-list-item-subtitle>
    </v-list-item-content>
    <v-spacer></v-spacer>
    <v-list-item-action class="flex-row">
      <BmInfoDialog v-on:data-change="emitChange" :bm="bm"></BmInfoDialog>
      <EditAccountDialog v-on:data-change="emitChange" :bm="bm"></EditAccountDialog>
      <DeleteAccountDialog v-on:data-change="emitChange" :bm="bm"></DeleteAccountDialog>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
  import Vue from 'vue'
  import BmInfoDialog from "@/components/BmInfoDialog.vue";
  import EditAccountDialog from "@/components/EditAccountDialog";
  import DeleteAccountDialog from "@/components/DeleteAccountDialog";

  export default Vue.extend({
    name: 'BmItem',
    components: {DeleteAccountDialog, EditAccountDialog, BmInfoDialog},
    props: {
      bm: Object
    },

    data: () => ({
    }),

    methods: {
      emitChange() {
        this.$emit('data-change')
      }
    }
  })
</script>
