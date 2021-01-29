<template>
  <div>
    <v-app-bar
      dense
      app
      elevation="3"
      elevate-on-scroll
      color="primary"
      class="user-menu"
    >
      <v-row align="center">
        <v-toolbar-title class="mr-3">
          <v-btn @click="$root.$emit('menu')" dark icon>
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </v-toolbar-title>
        <span v-if="!showSearchBar" class="nav-bar-title white--text">{{
          title
        }}</span>

        <v-text-field
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
    <v-app-bar elevate-on-scroll id="nav-bar" class="company" app color="white">
      <v-toolbar-title>
        <v-list-item
          dense
          id="logo-btn"
          class="mt-2 mb-2 pl-0 primary--text"
          one-line
          :to="{ path: '/' }"
        >
          <v-list-item-avatar>
            <v-img
              color="primary"
              src="@/assets/logo.png"
              max-height="35"
              max-width="35"
            >
            </v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>
              <h2 id="company-name" class="primary--text">COCO</h2>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-text-field
        dense
        class="pt-7 search-field"
        v-model="searchValue"
        @click:append="go2search"
        @keydown.enter="go2search"
        placeholder="Buscar trueques"
        solo
        append-icon="mdi-magnify"
      ></v-text-field>

      <v-spacer></v-spacer>
      <div v-if="!authentication.userIsAuthenticated && userRequireMoreInfo">
        <v-btn
          @click="updateFormsDialog(true, false)"
          class="mr-2"
          text
          color="primary darken-1"
        >
          Inicia sesión
        </v-btn>
        <v-btn @click="updateFormsDialog(false, true)" color="primary darken-1">
          Regístrate
        </v-btn>
        <Login v-if="forms.loginDialog" />
        <SignUp v-if="forms.signUpDialog" />
      </div>

      <v-btn v-else icon>
        <v-icon class="help-icon">mdi-help-circle-outline</v-icon>
      </v-btn>
    </v-app-bar>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import Login from "@/components/Login.vue";
import SignUp from "@/components/SignUp.vue";
export default {
  data: () => ({
    loginDialog: false,
    signUpDialog: false,
    searchValue: "",
    showSearchBar: false,
    title: "",
  }),
  components: {
    Login,
    SignUp,
  },
  watch: {
    $route(to, from) {
      if (to.name != "Explore") this.searchValue = "";
      this.setTitle();
    },
    profile(){
      this.setTitle();
    }
  },
  created() {
    if (this.$route.query.q) this.searchValue = this.$route.query.q;
    this.setTitle();
  },

  methods: {
    ...mapMutations(["updateFormsInfo"]),
    searchPubs() {
      console.log("searching..");
    },
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
      this.$router.push({ name: "Explore", query: { q: this.searchValue } });
    },
  },
  computed: {
    ...mapState(["authentication", "forms", "userRequireMoreInfo", "user", "profile"]),
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
#logo-btn {
  max-height: 30px;
}
</style>
