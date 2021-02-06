  <template>
  <div>
    <v-container fluid class="pa-0">
      <v-row justify="center">
        <v-col cols="3"  class="text-center">
          <v-btn @click="googleLogin" color="red darken-4" dark>
            <v-icon>mdi-google</v-icon>
            <span class="big-devices ml-1">Google</span>
          </v-btn>
        </v-col>
        <v-col cols="3"  class="text-center">
          <v-btn
            @click="socialBtn = 'Facebook'"
            color="blue darken-4"
            elevation="0"
          >
            <template>
              <v-facebook-login
                id="fb-btn"
                v-on:login="fbLogin"
                sdk-locale="es_LA"
                :options="{
                  cookie: false,
                  xfbml: true,
                  autoLogAppEvents: true,
                }"
                app-id="2895956430685783"
                class="pa-0 blue darken-4"
              >
                <v-icon class="big-devices" slot="logo">mdi-facebook</v-icon>
                <span class="big-devices ml-1" slot="login">FACEBOOK</span>
                <span class="big-devices ml-1" slot="working">Espere...</span>
              </v-facebook-login>
            </template>
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

  <script>
import { mapState, mapMutations } from "vuex";
import { setCookie } from "@/js/cookiesfunctions.js";
import VFacebookLogin from "vue-facebook-login-component";

export default {
  name: "SocialLogin",
  components: {
    VFacebookLogin,
  },
  data: () => ({
    apiDir: {
      google: "user-auth/google/",
      facebook: "user-auth/facebook/",
      twitter: "user-auth/twitter/",
      socialBtn: "",
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
          if (this.socialBtn == "Facebook") {
            this.simulateClick();
          }
          let responseObj = {
            accessToken: response.key,
            userIsAuthenticated: !!response.key,
          };
          setCookie("token", response.key, 60);
          this.updateAuthInfo(responseObj);
          this.updateFormsInfo(false, false);

          this.$router.push({ name: "Home" });
        })
        .catch((err) => {
          if (this.socialBtn == "Facebook") this.backendLogin();
        });
    },
    simulateClick() {
      var event = new MouseEvent("click", {
        view: window,
        bubbles: true,
        cancelable: true,
      });
      var cb = document.getElementById("fb-btn");
      cb.dispatchEvent(event);
    },
    fbLogin(fbResponse) {
      let accessToken = fbResponse.authResponse.accessToken;
      this.backendLogin(accessToken, this.apiDir.facebook);
    },
  },
  mounted() {},
};
</script>

  <style>
  #fb-btn:hover{
    cursor: pointer;
  }
</style>