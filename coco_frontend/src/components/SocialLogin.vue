<template>
  <div>
    <v-container fluid class="pa-0">
      <v-row justify="center">
        <v-col cols="3" class="text-center">
          <v-btn @click="googleLogin" color="red darken-4" dark>
            <v-icon>mdi-google</v-icon>
            <span class="big-devices ml-1">Google</span>
          </v-btn>
        </v-col>
        <v-col cols="3" sm="4" class="text-center">
          <v-btn color="blue darken-4" dark>
            <v-icon>mdi-facebook</v-icon>
            <span class="big-devices ml-1">Facebook</span>
          </v-btn>
        </v-col>
        <v-col cols="3" class="text-center">
          <v-btn color="blue" dark>
            <v-icon>mdi-twitter</v-icon>
            <span class="big-devices ml-1">Twitter</span>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { setCookie } from "@/js/cookiesfunctions.js";

export default {
  name: "SocialLogin",
  data: () => ({
    apiDir: {
      google: "user-auth/google/",
      facebook: "user-auth/facebook/",
      twitter: "user-auth/twitter/",
    },
  }),
  computed: {
    ...mapState(["baseUrl", "user"]),
  },
  methods: {
    ...mapMutations(["updateFormsInfo", "updateAuthInfo"]),

    googleLogin() {
      this.$gAuth
        .signIn()
        .then((googleUser) => {
          let accessToken = googleUser.getAuthResponse().access_token;
          this.backendLogin(accessToken, this.apiDir.google);
        })
        .catch((error) => {
          // On fail do something
        });
    },
    backendLogin(socialAuthToken, socialProvider) {
      let formData = {
        access_token: socialAuthToken,
        code: "",
      };
      fetch(this.baseUrl + socialProvider, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      })
        .then((response) => response.json())
        .then((response) => {
          let responseObj = {
            accessToken: response.key,
            userIsAuthenticated: !!response.key,
          };
          setCookie("token", response.key, 60);

          this.updateAuthInfo(responseObj);
          this.updateFormsInfo(false, false);
          this.$router.push({ name: "Home" });
        });
    },
  },
  mounted() {},
};
</script>

<style>
</style>