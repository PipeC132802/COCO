<template>
  <div class="pl-2">
    <v-row v-if="userContact.place" class="ml-1 mb-2">
      <span class="skills">
        <v-icon class="pb-1" left color="info"> mdi-earth </v-icon>
        Vive en {{ userContact.place }}
      </span>
    </v-row>
    <v-row v-if="userContact.skills" class="ml-1 mb-2">
      <span class="skills">
        <v-icon class="pb-1" left color="info"> mdi-teach </v-icon>
        {{ userContact.skills }}
      </span>
    </v-row>
    <v-row v-if="userContact.interests" class="ml-1 mb-2">
      <span class="skills">
        <v-icon class="pb-1" left color="info"> mdi-school </v-icon>
        {{ userContact.interests }}
      </span>
    </v-row>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data: () => ({
    userContact: {
      place: "",
      interests: "",
      skills: "",
    },
    apiDir: "user-contact/",
  }),
  computed: {
    ...mapState(["baseUrl", "authentication"]),
  },
  mounted() {
    this.getUserContactInfo();
    this.$root.$on("userInfoUpdated", () => {
      this.getUserContactInfo();
    });
  },
  methods: {
    getUserContactInfo() {
      let username = this.$route.params.username;
      fetch(this.baseUrl + this.apiDir + "?username=" + username, {})
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.userContact = response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style scoped>
span {
  font-size: 12pt;
  font-family: "Open Sans", "Segoe UI", "Roboto";
}
</style>
