<template>
  <v-app color="primary">
    <NavBar />
    <div
      @mouseenter="changeContainerSizes(255)"
      @mouseleave="changeContainerSizes(55)"
      style="background: black"
      v-if="authentication.userIsAuthenticated"
    >
      <LeftAside id="leftAside" />
    </div>
    <v-main id="content">
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import { readCookie } from "@/js/cookiesfunctions.js";
import LeftAside from "@/components/LeftAside";
import NavBar from "@/components/NavBar";

export default {
  name: "App",

  components: {
    NavBar,
    LeftAside,
  },

  data: () => ({}),
  beforeUpdate() {},
  beforeMount() {
    let aside = document.getElementById("leftAside");
    let token = readCookie("token");
    let responseObj = {
      accessToken: token,
      userIsAuthenticated: true,
    };
    this.updateAuthInfo(responseObj);
  },
  computed: {
    ...mapState(["authentication"]),
  },
  methods: {
    ...mapMutations(["updateAuthInfo"]),
    changeContainerSizes(size) {
      let container = document.getElementById("content");
      container.style = `padding-left: ${size}px; padding-top: 62px;`;
    },
  },
};
</script>

<style scoped>
#content {
  min-height: 100vh;
  width: 100%;
}
#container-body {
  background: white;
  margin: 20px auto;
}
</style>
