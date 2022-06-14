<template>
  <v-list-item two-line>
    <v-list-item-content>
      <v-list-item-title class="v-size--large mb-3">{{account.name}}</v-list-item-title>
      <v-list-item-subtitle>Id: {{account.id}}</v-list-item-subtitle>
    </v-list-item-content>
    <v-spacer></v-spacer>
    <v-list-item-action class="flex-row">
      <AccountInfoDialog v-on:data-change="emitChange" :account="account"></AccountInfoDialog>
      <EditAccountDialog v-on:data-change="emitChange" :account="account"></EditAccountDialog>
      <DeleteAccountDialog v-on:data-change="emitChange" :account="account"></DeleteAccountDialog>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
  import Vue from 'vue'
  import AccountInfoDialog from "@/components/AccountInfoDialog.vue";
  import EditAccountDialog from "@/components/EditAccountDialog";
  import DeleteAccountDialog from "@/components/DeleteAccountDialog";

  export default Vue.extend({
    name: 'AccountItem',
    components: {DeleteAccountDialog, EditAccountDialog, AccountInfoDialog},
    props: {
      account: Object
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
