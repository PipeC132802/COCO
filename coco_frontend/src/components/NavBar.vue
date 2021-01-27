<template>
  <div>
    <v-app-bar id="nav-bar" app color="white">
      <v-toolbar-title>
        <v-list-item
          id="logo-btn"
          class="mt-2 mb-2 pl-3 primary--text"
          one-line
          :to="{path:'/'}"
        >
          <v-list-item-avatar>
            <v-img color="primary" src="@/assets/logo.png" max-height="35" max-width="35">
            </v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title >
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
          @click="updateFormsDialog(true,false)"
          class="mr-2"
          text
          color="primary darken-1"
        >
          Inicia sesión
        </v-btn>
        <v-btn
          @click="updateFormsDialog(false,true)"
          color="primary darken-1"
        >
          Regístrate
        </v-btn>
        <Login v-if="forms.loginDialog"  />
        <SignUp v-if="forms.signUpDialog"  />
      </div>

      <v-btn v-else icon>
        <v-icon>mdi-help-circle-outline</v-icon>
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
    searchValue: '',
  }),
  components: {
    Login,
    SignUp
  },
  watch: {
    $route(to, from) {
      if(this.$route.name != 'Explore') this.searchValue = '';
    },
  },
  created(){
    if(this.$route.query.q) this.searchValue = this.$route.query.q;
  },
  methods: {
    ...mapMutations(["updateFormsInfo"]),
    searchPubs() {
      console.log("searching..");
    },
    
    updateFormsDialog(login,signup){
      let formDialog = {
        loginDialog: login,
        signUpDialog: signup
      }
      
      this.updateFormsInfo(formDialog)
    },
    go2search(){
      this.$router.push({name:'Explore',query:{q:this.searchValue}});
    },
  },
  computed: {
    ...mapState(["authentication", "forms","userRequireMoreInfo"]),
  },
};
</script>

<style>
@media (max-width: 920px) {
  .search-field {
    display: none;
  }
  #nav-bar{
    left: 0% !important;
    position: fixed;
    background: #307ABD  !important;
  }

  #company-name{
    color: white  !important;
  }
}
#logo-btn {
  max-height: 30px;
}

</style>
