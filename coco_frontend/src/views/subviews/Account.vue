<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col class="pb-0 pt-0 mb-0" cols="12">
          <h2 class="title--text">Tu cuenta</h2>
          <p>
            <v-divider></v-divider>
          </p>
          <p class="grey--text">
            Navega entre las diferentes opciones que tenemos para que
            administres tu cuenta.
          </p>
        </v-col>
        <v-col class="pt-0" cols="12">
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
};
</script>

<style>
</style>