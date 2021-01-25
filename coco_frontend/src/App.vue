<template>
  <v-app color="primary">
    <NavBar />
    <div
      @mouseenter="changeContainerSizes(255)"
      @mouseleave="changeContainerSizes(55)"
      v-if="authentication.userIsAuthenticated"
    >
      <LeftAside id="leftAside" />
    </div>
    <v-main id="content">
      <router-view />
    </v-main>
    <div class="notifications">
        <NotificationBox v-for="(notification, index) in notifications" :key="index" :notification="notification" />
    </div>
  </v-app>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import { readCookie } from "@/js/cookiesfunctions.js";
import LeftAside from "@/components/LeftAside.vue";
import NavBar from "@/components/NavBar.vue";
import NotificationBox from "@/components/NotificationBox.vue";

export default {
  name: "App",

  components: {
    NavBar,
    LeftAside,
    NotificationBox
  },

  data: () => ({
    list: ['Hola']
  }),
  watch: {},
  beforeUpdate() {},
  beforeMount() {
    let aside = document.getElementById("leftAside");
    let token = readCookie("token");
    let responseObj = {
      accessToken: token,
      userIsAuthenticated: !!token,
    };
    this.updateAuthInfo(responseObj);
  },
  computed: {
    ...mapState(["authentication","notifications"]),
  },
  methods: {
    ...mapMutations(["updateAuthInfo"]),
    changeContainerSizes(size) {
      let container = document.getElementById("content");
      container.style = `padding-left: ${size}px; padding-top: 62px;`;
    },
    listMela(val){
      this.list.pop(val)
    }
  },
};
</script>

<style>
@media (max-width: 920px) {
  #leftAside {
    display: none;
  }
  #content{
    padding: 0px 0px !important;
  }
  p, span{
    font-size: 10pt;
  }
}
body {
  background: rgb(211, 211, 211);
}
#content {
  min-height: 100vh;
  width: 100%;
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
.notifications{
  position: fixed;
  right: 10px;
  bottom: 10px;
  width: 350px;
  z-index: 100;
  display: flex;
  flex-direction: column-reverse;
}
</style>
