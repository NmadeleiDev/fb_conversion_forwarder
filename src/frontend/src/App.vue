<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-img
          alt="Vuetify Logo"
          class="shrink mr-2"
          contain
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
          transition="scale-transition"
          width="40"
        />

        <v-img
          alt="Vuetify Name"
          class="shrink mt-1 hidden-sm-and-down"
          contain
          min-width="100"
          src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
          width="100"
        />
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
        text
      >
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>

      <v-btn
        @click="emitEvent"
      >
      TEST
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>

    </v-app-bar>

    <v-main>
      <HelloWorld/>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue';
import HelloWorld from './components/HelloWorld.vue';
function xFbConvSend(event_name,emails=[],phones=[],genders=[],last_names=[],first_names=[],cities=[],countries=[],dates_of_birth=[]){const it="2.C36R9vMQ0Sej65RhCOn96wc5WtJkVvjP";try{let fbc=null;let fbp=null;document.cookie.split(";").map((x=>x.trim())).forEach((x=>{const parts=x.split("=");if(parts[0]=="_fbc")fbc=parts[1];if(parts[0]=="_fbp")fbp=parts[1]}));const body={auth_token:it,event_name:event_name,event_time:Math.floor(Number(new Date)/1e3),emails:emails,phones:phones,genders:genders,last_names:last_names,first_names:first_names,dates_of_birth:dates_of_birth,cities:cities,countries:countries,fbc:undefined,fbp:undefined};if(fbc)body.fbc=fbc;if(fbp)body.fbp=fbp;fetch("http://localhost:8092/api/v1/fw/c",{method:"POST",mode:"cors",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)}).then((x=>console.log(x)))}catch(e){console.log(e)}}

export default Vue.extend({
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    //
  }),
  methods: {
    emitEvent() {
      console.log('start')
      xFbConvSend('test_event')
    }
  }
});
</script>
