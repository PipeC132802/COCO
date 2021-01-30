<template>
  <div>
    <v-container>
      <v-row>
        <v-col v-if="mainMenu" cols="12" sm="12" md="4">
          <div class="px-3 mb-0 title--text settings-title">
            <strong>Ajustes</strong>
          </div>
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
        <v-divider v-if="mainMenu" vertical></v-divider>
        <v-col class="ma-0 pa-0" cols="12" sm="12" md="7">
          <router-view v-on:main="updateMenuVisibility" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Settings",
  data: () => ({
    menu: [
      { title: "Tu cuenta", link: "Account" },
      { title: "Privacidad y Seguridad", link: "Security" },
      { title: "Notificaciones", link: "NotificationsSettings" },
      { title: "Recursos", link: "Resources" },
    ],
    mainMenu: true,
  }),
  computed: {
    ...mapState(["breakpoints"]),
  },
  created() {
    document.title = "Ajustes | COCO";
  },
  watch: {
    $route(from, to) {
      let screenWidth = window.screen.width;
      if (this.breakpoints.xs > screenWidth && this.$route.name != "Settings") {
        this.mainMenu = false;
      } else {
        this.mainMenu = true;
      }
    },
  },
  methods: {
    updateMenuVisibility(visibility) {
      this.mainMenu = visibility;
    },
  },
};
</script>

<style>
* {
  padding: 0%;
  margin: 0%;
}
.arrow-back {
  display: none;
}
.settings-title {
  font-size: calc(1em + 1vw);
}
@media (max-width: 920px) {
  .arrow-back {
    display: block;
  }
}
</style>