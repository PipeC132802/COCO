<template>
  <div v-if="!authentication.userIsAuthenticated">
  gg
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  name: "Welcome",
  created() {},
  computed: {
    ...mapState(["authentication", "userRequireMoreInfo"]),
  },
  created() {
    if (!this.userRequireMoreInfo) {
      this.$router.push({ name: "MoreInfo" });
    }
    if (this.authentication.userIsAuthenticated) {
      this.$router.push({ name: "Home" });
    }
  },
  mounted() {
    let btn = document.getElementById("logo-btn");
    let navBar = document.getElementsByClassName("company");
    btn.classList.remove("v-list-item--active");
    console.log(navBar);
    navBar.forEach((element) => {
      element.classList.add("init");
      console.log(element);
    });
  },
  methods: {},
};
</script>
<style>
</style>