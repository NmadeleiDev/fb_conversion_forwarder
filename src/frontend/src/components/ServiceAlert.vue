<template>
  <v-alert dismissible
           v-model="val"
           type="error"
  >{{content}}</v-alert>
</template>

<script>
export default {
  name: "ServiceAlert",

  props: {
    val: Boolean,
    content: String
  }
}
</script>

<style scoped>

</style>