<template>
  <div>
    <v-navigation-drawer
      permanent
      app
      color="primary"
      class="navigation pa-0 ma-0"
      dark
      expand-on-hover
      v-if="authentication.userIsAuthenticated"
    >
      <template v-slot:prepend class="ma-0">
        <v-list-item class="pa-0 pl-2 ma-0" two-line>
          <v-list-item-avatar size="30" color="secondary" class="mt-4 ml-1">
            <img
              v-if="user.profile_picture"
              :alt="'perfil de ' + user.name"
              :src="user.profile_picture"
            />
            <span class="white--text" v-else>{{
              user.name.slice(0, 1).toUpperCase()
            }}</span>
          </v-list-item-avatar>
          <v-list-item-content class="white--text">
            <v-list-item-title :title="user.name">{{
              user.name
            }}</v-list-item-title>
            <v-list-item-subtitle
              :title="'@' + user.username"
              class="secondary--text"
              >@{{ user.username }}</v-list-item-subtitle
            >
          </v-list-item-content>
        </v-list-item>
      </template>
      <v-divider dark></v-divider>

      <v-list dense>
        <v-list-item
          class="item"
          :title="item.title"
          active-class="white primary--text"
          :to="{ path: `${item.link}` }"
          exact
          v-for="item in items"
          :key="item.title"
          link
        >
          <v-list-item-icon>
            <v-badge
              :content="item.value"
              :value="item.value"
              color="accent"
              overlap
            >
              <v-icon>{{ item.icon }}</v-icon>
            </v-badge>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-list-item
        dense
        @click="closeSession()"
        class="logout error darken-1"
        link
      >
        <v-list-item-icon>
          <v-icon>mdi-logout-variant</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Cerrar Sesión</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-navigation-drawer>

    <v-navigation-drawer
      class="navigation-small-device"
      v-model="drawerSmall"
      absolute
      left
      temporary
      :right="authentication.userIsAuthenticated ? false : true"

    >
      <v-list nav dense v-if="authentication.userIsAuthenticated">
        <v-list-item-group active-class="primary--text text--accent-4">
          <v-list-item
            :to="{ name: 'Profile', params: { username: user.username } }"
            class="pa-0 pl-2 ma-0"
            two-line
          >
            <v-list-item-avatar size="30" color="secondary" class="mt-4 ml-1">
              <img
                v-if="user.profile_picture"
                :alt="'perfil de ' + user.name"
                :src="user.profile_picture"
              />
              <span class="white--text" v-else>{{
                user.name.slice(0, 1).toUpperCase()
              }}</span>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title class="primary--text" :title="user.name">
                <strong>{{ user.name }}</strong>
              </v-list-item-title>
              <v-list-item-subtitle
                :title="'@' + user.username"
                class="secondary--text"
                >@{{ user.username }}</v-list-item-subtitle
              >
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
        <v-list-item
          title="Perfil"
          class="mt-2"
          active-class="primary white--text"
          :to="{ name: 'Profile', params: { username: user.username } }"
          exact
          link
        >
          <v-list-item-icon>
            <v-icon>mdi-account</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Perfil</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          title="Ajustes"
          active-class="primary white--text"
          :to="{ name: 'Settings' }"
          exact
          link
        >
          <v-list-item-icon>
            <v-icon>mdi-cogs</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>Ajustes</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          title="Cerrar sesión"
          @click="closeSession()"
          class="error darken-1"
          exact
          link
        >
          <v-list-item-icon>
            <v-icon color="white">mdi-logout-variant</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="white--text"
              >Cerrar sesión</v-list-item-title
            >
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <v-list v-else>
        <v-list-item>
          <v-list-item-title color="primary">
            <v-btn @click="$root.$emit('loginOrSingUpForm', true, false)" block color="primary" outlined>
              <v-icon left>mdi-login</v-icon>

              Iniciar sesión
            </v-btn>
          </v-list-item-title>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>
            <v-btn @click="$root.$emit('loginOrSingUpForm', false, true)" block color="primary">
              <v-icon left>mdi-account-plus</v-icon>
              Regístrate
            </v-btn>
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { removeCookie } from "@/js/cookiesfunctions.js";
export default {
  name: "LeftAside",
  data: () => ({
    user: {
      profile_picture: "",
      name: "",
      username: "",
    },
    apiDir: "user-status/",
    logOutApi: "user-auth/logout/",
    drawer: true,
    drawerSmall: true,
    group: null,
    items: [
      { title: "Inicio", icon: "mdi-home", link: "/home", value: "" },
      { title: "Explorar", icon: "mdi-magnify", link: "/search", value: "" },
      {
        title: "Notificaciones",
        icon: "mdi-bell",
        link: "/notifications",
        value: "",
      },
      {
        title: "Mensajes",
        icon: "mdi-message-text",
        link: "/inbox",
        value: "",
      },
      { title: "Perfil", icon: "mdi-account", link: "/profile", value: "" },
      { title: "Ajustes ", icon: "mdi-cogs", link: "/settings", value: "" },
    ],
    notifications_box: [],
    mini: true,
  }),
  watch: {
    group() {
      this.drawer = false;
    },
    authentication(){
      this.getUserInfo();
    },
    notification(){
      this.items[3].value = this.notification.unread_messages;
    }
  },
  computed: {
    ...mapState(["baseUrl", "authentication", "wsBase", "notification"]),
  },
  mounted() {
    this.getUserInfo();
    this.$root.$on("notificationsReaded", () => {
      this.items[2].value = 0;
    });
    this.$root.$on("menu", () => {
      this.drawerSmall = !this.drawerSmall;
    });
  },

  methods: {
    ...mapMutations([
      "setUser",
      "updateAuthInfo",
      "addNotification",
      "notificationStatus",
    ]),
    getUserInfo() {
      fetch(this.baseUrl + this.apiDir, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((respose) => {
          return respose.json();
        })
        .then((respose) => {
          this.user = respose;
          this.items[2].value = respose.unread_notifications;
          this.items[3].value = respose.unread_messages;
          this.items[4].link = `/${respose.username}`;
          this.notificationStatus({
            unread_notifications: respose.unread_notifications,
            unread_messages: respose.unread_messages,
          });
          this.setUser(respose);

          this.$root.$emit("userSetted");

          this.connect();
        });
    },
    closeSession() {
      let authObj = {
        accessToken: null,
        userIsAuthenticated: false,
      };
      //this.deleteToken(); This unauthenticate all users
      removeCookie("token");
      this.updateAuthInfo(authObj);
      this.setUser("");
      this.$router.push({ name: "Welcome" });
    },
    connect() {
      let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";
      this.websocket = new WebSocket(
        protocol + this.wsBase + "/ws/notifications/" + this.user.username + "/"
      );
      this.websocket.onopen = () => {
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));
          const socketData = JSON.parse(data);
          if (socketData.type == "new_notification") {
            this.items[2].value = socketData.unread_notifications;
            this.notificationStatus({
              unread_notifications: socketData.unread_notifications,
              unread_messages: this.items[3].value,
            });
          }
          this.addNotification(socketData);
        };
      };
      this.websocket.onclose = () => {};
    },
  },
};
</script>
<style scoped>
.navigation {
  color: white;
}
.item {
  border-radius: 15px;
  height: 50px;
  padding-top: 5px;
}
.logout {
  position: absolute;
  bottom: 0;
  width: 100%;
  border-radius: 10px 10px 0px 0;
}
@media (max-width: 920px) {
  .navigation {
    display: none;
  }
  .navigation-small-device {
    display: block;
    top: 0px;
  }
}
@media (min-width: 920px) {
  .navigation {
    display: block;
  }
  .navigation-small-device {
    display: none;
  }
}
</style>