<template>
    

    <v-app color="primary">
      <router-view v-if="$route.name == 'VerifyEmail'" />
      <div v-else>

      <NavBar />
      <div
        @mouseenter="changeContainerSizes(255)"
        @mouseleave="changeContainerSizes(55)"
      >
        <LeftAside id="leftAside" />
      </div>
      <v-main
        :class="authentication.userIsAuthenticated ? '' : 'px-12'"
        id="content"
      >
        <router-view />
      </v-main>
      <div class="notifications">
        <NotificationBox
          v-for="(notification, index) in notifications"
          :key="index"
          :notification="notification"
        />
      </div>
      <v-fab-transition
        v-if="floatingIcon && authentication.userIsAuthenticated"
      >
        <v-btn
          color="primary"
          fab
          dark
          right
          elevation="3"
          id="btn-create"
          bottom
          fixed
          @click="setFloatingBtnEvent"
        >
          <v-icon>{{ floatingIcon }}</v-icon>
        </v-btn>
      </v-fab-transition>
      <FooterNav v-if="authentication.userIsAuthenticated" class="footer-nav" />
      <div v-if="authentication.userIsAuthenticated" id="notification"></div>
            </div>

    </v-app>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import { readCookie } from "@/js/cookiesfunctions.js";
import LeftAside from "@/components/LeftAside.vue";
import NavBar from "@/components/NavBar.vue";
import NotificationBox from "@/components/NotificationBox.vue";
import FooterNav from "@/components/FooterNav.vue";

export default {
  name: "App",

  components: {
    NavBar,
    LeftAside,
    NotificationBox,
    FooterNav,
  },

  data: () => ({
    floatingIcon: "mdi-pencil",
    apiDir: "user-status/",
    sound: require("@/assets/sounds/notifications/newmessage.ogg"),
  }),
  watch: {
    $route(from, to) {
      if (
        this.$route.name == "Messages" ||
        this.$route.name == "Inbox" ||
        this.$route.name == "ComposeBarter" ||
        this.$route.name == "Edit"
      )
        this.floatingIcon = false;
      else this.floatingIcon = "mdi-pencil";
    },
    authentication() {},
  },
  mounted() {
    this.$root.$on("newMewssage", () => {
      this.play();
    });
  },
  beforeMount() {
    let token = readCookie("token");
    if (token) {
      let responseObj = {
        accessToken: token,
        userIsAuthenticated: !!token,
      };
      this.updateAuthInfo(responseObj);
    }
  },
  computed: {
    ...mapState(["authentication", "notifications", "baseUrl"]),
  },
  methods: {
    ...mapMutations(["updateAuthInfo", "setUser"]),
    changeContainerSizes(size) {
      let container = document.getElementById("content");
      container.style = `padding-left: ${size}px; padding-top: 62px;`;
    },
    setFloatingBtnEvent() {
      if (this.floatingIcon && this.floatingIcon == "mdi-pencil") {
        this.$router.push({ name: "ComposeBarter" });
      } else if (this.floatingIcon && this.floatingIcon == "mdi-message-plus") {
        this.$root.$emit("createChat");
      }
    },
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
          this.setUser(respose);
          this.$root.$emit("userSetted");
        });
    },
    play() {
      let notificationDiv = document.getElementById("notification");
      notificationDiv.innerHTML = `<audio src="${this.sound}" autoplay></audio>`;
    },
  },
};
</script>

<style>
.big-devices {
  display: block;
}
.small-device {
  display: none;
}
@media (max-width: 920px) {
  #content {
    padding: 40px 0px 0px 0px !important;
  }
  p,
  span {
    font-size: 10pt;
  }
  .footer-nav {
    display: block;
  }
  #btn-create {
    bottom: 60px;
    z-index: 3;
  }
  .big-devices {
    display: none;
  }
  .small-device {
    display: block;
  }
}
@media (min-width: 920px) {
  .footer-nav {
    display: none;
  }
  #content {
    min-height: 100vh;
    width: 100%;
    padding-top: 60px !important;
  }
  #btn-create {
    display: none;
  }
}
body {
  background: rgb(211, 211, 211);
}

#container-body {
  margin: 20px auto;
}
link {
  text-decoration: none;
}
link:hover {
  text-decoration: underline;
}
.notifications {
  position: fixed;
  right: 10px;
  bottom: 10px;
  width: 350px;
  z-index: 100;
  display: flex;
  flex-direction: column-reverse;
}
#app {
  overflow-x: hidden;
}
</style>
