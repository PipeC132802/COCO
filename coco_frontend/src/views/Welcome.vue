<template>
  <div v-if="!authentication.userIsAuthenticated">
    <h1>Welcome</h1>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  name: "Welcome",
  created() {},
  computed: {
    ...mapState(["authentication","userRequireMoreInfo"]),
  },
  created() {
    if(!this.userRequireMoreInfo){
      this.$router.push({name: 'MoreInfo'})
    }
    if(this.authentication.userIsAuthenticated ) {
      this.$router.push({ name: "Home" });
    }
  },
  mounted() {
    let navBar = document.getElementById("logo-btn");
    navBar.classList.remove("v-list-item--active");
  },
  methods: {
  },
};
</script>