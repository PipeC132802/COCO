<template>
  <div>
    <v-container fluid>
      <div class="title--text settings-title px-3 mt-1 mb-2">
        <v-row align="center" class="pl-3 pt-3">
          <v-btn
            @click="$router.push({ name: 'Settings' })"
            class="mr-3 arrow-back"
            icon
            color="primary"
          >
            <v-icon> mdi-arrow-left </v-icon>
          </v-btn>
          Notificaciones
        </v-row>
      </div>
      <v-divider></v-divider>
      <p class="grey--text px-4 mb-1 mt-2">
        Establece las preferencias para tus notificationes.
      </p>
      <v-row>
        <v-col class="pt-2" cols="12">
          <v-list subheader one-line>
            <v-list-item active-class="primary white--text" class="pa-1 px-3">
              <v-list-item-avatar>
                <v-icon v-html="menu[0].icon"></v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-html="menu[0].title"></v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch
                  @change="updateNotificationPreferences"
                  v-model="notificationPush"
                ></v-switch>
              </v-list-item-action>
            </v-list-item>
            <v-list-item active-class="primary white--text" class="pa-1 px-3">
              <v-list-item-avatar>
                <v-icon v-html="menu[1].icon"></v-icon>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-html="menu[1].title"></v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch
                  @change="updateNotificationPreferences"
                  v-model="notificationEmail"
                ></v-switch>
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
  name: "Notifications",
  data: () => ({
    notificationPush: false,
    notificationEmail: false,
    menu: [
      {
        title: "Notificaciones push",
        icon: "mdi-bell",
      },
      {
        title: "Notificaciones por correo electrónico",
        icon: "mdi-email",
      },
    ],
    apiDir: "notifications-preferences/",
  }),
  computed: {
    ...mapState(["user", "authentication", "baseUrl", "breakpoints"]),
  },
  mounted() {
    this.getNotificationsPreferences();
    let screenWidth = window.screen.width;
    if (this.breakpoints.sm > screenWidth) {
      this.$emit("main", false);
    } else {
      this.$emit("main", true);
    }
  },
  methods: {
    getNotificationsPreferences() {
      fetch(this.baseUrl + this.apiDir, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          this.notificationPush = response.push;
          this.notificationEmail = response.email;
        });
    },
    updateNotificationPreferences() {
      let formData = {
        push: this.notificationPush,
        email: this.notificationEmail,
        sms: true,
      };
      fetch(this.baseUrl + this.apiDir, {
        method: "PUT",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
    },
  },
};
</script>

<style>
</style>