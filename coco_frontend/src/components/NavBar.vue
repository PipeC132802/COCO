  <template>
  <div>
    <div class="big-devices">
      <v-app-bar elevate-on-scroll class="company" app :color="toolbarColor">
        <v-toolbar-title>
          <v-list-item
            dense
            class="mt-2 mb-2 pl-0 primary--text logo-btn"
            one-line
            :to="{ path: '/' }"
          >
            <v-img
              color="primary"
              src="@/assets/logo.png"
              max-height="35"
              max-width="35"
            >
            </v-img>
            <v-list-item-content class="big-devices">
              <v-list-item-title>
                <h2 id="company-name" class="primary--text ml-2">COCO</h2>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-toolbar-title>
        <v-spacer class="big-devices"></v-spacer>
        <v-text-field
          dense
          class="pt-7"
          solo
          v-model="searchValue"
          @click:append="go2search"
          @keydown.enter="go2search"
          placeholder="Buscar trueques"
          append-icon="mdi-magnify"
        ></v-text-field>
        <v-spacer></v-spacer>
        <div
          class="mr-3"
          v-if="!authentication.userIsAuthenticated && userRequireMoreInfo"
        >
          <v-row>
            <v-btn
              @click="updateFormsDialog(true, false)"
              class="mr-2 big-devices"
              color="white primary--text"
            >
              Inicia sesión
            </v-btn>
            <v-btn
              @click="updateFormsDialog(false, true)"
              class="big-devices"
              color="primary darken-1"
            >
              Regístrate
            </v-btn>
          </v-row>

          <v-btn
            @click="showMenu"
            icon
            color="primary"
            class="small-device ml-3"
          >
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </div>
        <v-btn v-else @click="bugDialog = true" icon>
          <v-icon title="Reportar un bug" color="error" class="help-icon"
            >mdi-bug</v-icon
          >
        </v-btn>
      </v-app-bar>
    </div>
    <div class="small-device">
      <v-app-bar
        v-if="authentication.userIsAuthenticated"
        dense
        app
        elevation="3"
        elevate-on-scroll
        color="primary"
        class="user-menu"
      >
        <v-row align="center">
          <v-toolbar-title>
            <v-btn @click="$root.$emit('menu')" dark icon>
              <v-icon>mdi-menu</v-icon>
            </v-btn>
          </v-toolbar-title>
          <span v-if="!showSearchBar" class="nav-bar-title white--text">{{
            title
          }}</span>

          <v-text-field
            class="pt-6"
            v-if="showSearchBar"
            dense
            v-model="searchValue"
            @click:prepend="go2search"
            @keydown.enter="go2search"
            placeholder="Buscar trueques"
            solo
            prepend-inner-icon="mdi-magnify"
          ></v-text-field>
        </v-row>
      </v-app-bar>
      <v-app-bar
        v-else
        elevate-on-scroll
        class="company"
        app
        :color="toolbarColor"
      >
        <v-toolbar-title>
          <v-list-item
            dense
            class="mt-2 mb-2 pl-0 primary--text logo-btn"
            one-line
            active-class="transparent"
            :to="{ path: '/' }"
          >
            <v-img
              color="primary"
              src="@/assets/logo.png"
              max-height="35"
              max-width="35"
            >
            </v-img>
          </v-list-item>
        </v-toolbar-title>
        <v-text-field
          dense
          class="pt-7"
          solo
          v-model="searchValue"
          @click:append="go2search"
          @keydown.enter="go2search"
          placeholder="Buscar trueques"
          append-icon="mdi-magnify"
        ></v-text-field>

        <v-btn @click="showMenu" icon color="primary" class="small-device ml-3">
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </v-app-bar>
    </div>

    <Login v-if="forms.loginDialog" />
    <SignUp v-if="forms.signUpDialog" />
    <v-dialog width="500" v-model="bugDialog">
      <v-card> 
        <Bug v-on:closeBug="bugDialog=false;" />
      </v-card>
    </v-dialog>
  </div>
</template>

  <script>
import { mapState, mapMutations } from "vuex";
import Login from "@/components/Login.vue";
import SignUp from "@/components/SignUp.vue";
import Bug from "../components/Bug.vue";
export default {
  data: () => ({
    loginDialog: false,
    signUpDialog: false,
    bugDialog: false,
    searchValue: "",
    showSearchBar: false,
    title: "",
    screenWidth: window.screen.width,
    toolbarColor: "white",
  }),
  components: {
    Login,
    SignUp,
    Bug
  },
  computed: {
    ...mapState([
      "authentication",
      "forms",
      "userRequireMoreInfo",
      "user",
      "profile",
      "breakpoints",
    ]),
  },
  watch: {
    $route(to, from) {
      if (to.name != "Explore") this.searchValue = "";
      this.setTitle();
    },
    profile() {
      this.setTitle();
    },
  },
  created() {
    if (this.$route.query.q) this.searchValue = this.$route.query.q;
    this.setTitle();
  },
  mounted() {
    this.$root.$on("loginOrSingUpForm", (lg, sp) => {
      this.updateFormsDialog(lg, sp);
    });
    this.$root.$on("toolBarColor", (color) => {
      this.toolbarColor = color;
    });
  },

  methods: {
    ...mapMutations(["updateFormsInfo"]),
    setTitle() {
      if (this.$route.name != "Explore") {
        this.showSearchBar = false;
        if (this.$route.name == "Home") {
          this.title = "Inicio";
        } else if (this.$route.name == "Notifications") {
          this.title = "Notificaciones";
        } else if (
          this.$route.name == "Inbox" ||
          this.$route.name == "Messages"
        ) {
          this.title = "Mensajes";
        } else if (this.$route.name == "Profile") {
          this.title = this.profile.name;
        } else if (this.$route.name == "Barter") {
          this.title = "Trueque";
        } else if (this.$route.name == "Settings") {
          this.title = "Ajustes";
        } else if (this.$route.name == "ComposeBarter") {
          this.title = "Nuevo trueque";
        }
      } else {
        this.showSearchBar = true;
      }
    },
    updateFormsDialog(login, signup) {
      let formDialog = {
        loginDialog: login,
        signUpDialog: signup,
      };

      this.updateFormsInfo(formDialog);
    },
    go2search() {
      if (this.searchValue.trim())
        this.$router.push({ name: "Explore", query: { q: this.searchValue } });
    },
    showMenu() {
      this.$root.$emit("menu");
    },
  },
};
</script>

  <style>
@media (max-width: 920px) {
  .search-field {
    display: none;
  }
  #nav-bar {
    display: none;
  }
  .user-menu {
    display: block;
    left: 0px !important;
  }
  .nav-bar-title {
    font-size: 16pt;
    color: rgb(226, 226, 226);
    width: calc(100vw - 100px);
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
  }
}
@media (min-width: 920px) {
  .user-menu {
    display: none;
  }
  .company {
    display: block;
  }
}
.logo-btn {
  max-height: 30px;
}
</style>
