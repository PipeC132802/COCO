<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="4">
          <div class="px-3 mb-0 title--text display-1">Ajustes</div>
          <p>

          <v-divider></v-divider>
          </p>
          <v-list subheader one-line>
            <v-list-item
              v-for="item in menu"
              :key="item.title"
              :to="{ name: item.link }"
              exact
              active-class="primary white--text"
              class="pa-1 px-3"
            >
              <v-list-item-content>
                <v-list-item-title v-html="item.title"></v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-icon>mdi-chevron-right</v-icon>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-col>
        <v-divider vertical></v-divider>
        <v-col class="ma-0 pa-0" cols="7">
          <router-view />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "Settings",
  data: () => ({
    menu: [
      { title: "Tu cuenta", link: "Account" },
      { title: "Privacidad y Seguridad", link: "Security" },
      { title: "Notificaciones", link: "NotificationsSettings" },
      { title: "Recursos", link: "Resources" },
    ],
  }),
  created() {
    document.title = "Ajustes | COCO";
  },
};
</script>

<style>
*{
  padding: 0%;
  margin: 0%;
}
</style>