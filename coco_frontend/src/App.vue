<template>
  <v-app color="primary">
        <NavBar />
    <div
      @mouseenter="changeContainerSizes(255)"
      @mouseleave="changeContainerSizes(55)"
      style="background: black"
    >
      <LeftAside id="leftAside" />
    </div>
    <v-main id="content">
        <router-view />
    </v-main>
  </v-app>
</template>

<script>
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
  created() {
    let aside = document.getElementById("leftAside");
  },
  methods: {
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
#container-body{
  background: white;
  widows: 90%;
  margin: 20px auto;
}

</style>
