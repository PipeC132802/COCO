<template>
  <div>
    <v-container fluid>
      <div class="title--text settings-title px-3">
        <v-row align="center" class="pl-3 pt-2">
          <v-btn
            @click="$router.push({ name: 'Settings' })"
            class="mr-3 arrow-back"
            icon
            color="primary"
          >
            <v-icon> mdi-arrow-left </v-icon>
          </v-btn>
          Tu cuenta
        </v-row>
      </div>
      <v-divider></v-divider>
      <p class="grey--text  px-4 mb-1">
        Navega entre las diferentes opciones que tenemos para que administres tu
        cuenta.
      </p>
      <v-row>
        <v-col class="pt-2" cols="12">
          <v-list subheader one-line>
            <v-list-item
              v-for="item in menu"
              :key="item.title"
              :to="{ name: item.link }"
              exact
              active-class="primary white--text"
              class="pa-1 px-3"
            >
              <v-list-item-avatar>
                <v-icon v-html="item.icon"></v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-html="item.title"></v-list-item-title>
                <v-list-item-subtitle
                  v-html="item.subtitle"
                ></v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon>mdi-chevron-right</v-icon>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import {mapState} from "vuex";
export default {
  name: "Account",
  data: () => ({
    menu: [
      {
        title: "Tu información",
        subtitle: "Mira tu información como nombre, correo electrónico, etc.",
        link: "YourInfo",
        icon: "mdi-account",
      },
      {
        title: "Contraseña",
        subtitle: "Actualiza tu contraseña para mantener tu cuenta protegida.",
        link: "Password",
        icon: "mdi-key",
      },
      {
        title: "Desactiva tu cuenta",
        subtitle: "Mira cómo puedes desactivar tu cuenta.",
        link: "Deactivate",
        icon: "mdi-heart-broken",
      },
    ],
  }),
  computed: {
    ...mapState(["breakpoints"])
  },
  mounted(){
    let screenWidth = window.screen.width;
      if(this.breakpoints.sm > screenWidth){
        this.$emit("main", false)
      } else {
        this.$emit("main", true)
      }
  }
};
</script>

<style>
</style>