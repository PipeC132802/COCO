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
          Privacidad y seguridad
        </v-row>
      </div>
      <v-divider></v-divider>
      <p class="grey--text px-4 mb-1 mt-2">
        Establece qué información ves y compartes en COCO y administra la
        seguridad de tu cuenta.
      </p>
      <v-row>
        <v-col class="pt-2" cols="12">
          <v-list subheader one-line>
            <v-list-item
              v-for="item in menu"
              :key="item.title"
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
import { mapState } from "vuex";
export default {
  name: "Security",
  data: () => ({
    menu: [
      {
        title: "Bloquear",
        subtitle: "Añade usuarios a tu lista de bloqueo.",
        link: "#",
        icon: "mdi-lock",
      },
      {
        title: "Sesiones",
        subtitle: "Mira las sesiones realizadas a tu cuenta de COCO.",
        link: "#",
        icon: "mdi-cellphone-link",
      },
    ],
  }),
  mounted() {
    let screenWidth = window.screen.width;
    if (this.breakpoints.sm > screenWidth) {
      this.$emit("main", false);
    } else {
      this.$emit("main", true);
    }
  },
  computed: {
    ...mapState(["breakpoints"]),
  },
};
</script>

<style>
</style>