<template>
  <div>
    <v-app-bar app color="white">
      <v-toolbar-title>
        <v-list-item
          id="logo-btn"
          color="primary--text"
          exact
          class="mt-2 mb-2 pl-3"
          one-line
          :to="{path:'/'}"
        >
          <v-list-item-avatar>
            <v-img src="@/assets/logo.png" max-height="35" max-width="35">
            </v-img>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title class="primary--text">
              <h2>COCO</h2>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-text-field
        dense
        class="pt-7"
        label="Solo"
        @click:append="searchPubs"
        placeholder="¿Trueque o miedo?"
        solo
        append-icon="mdi-magnify"
      ></v-text-field>

      <v-spacer></v-spacer>
      <div v-if="!authentication.userIsAuthenticated">
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

      <v-btn v-else icon class="mr-3">
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
  }),
  components: {
    Login,
    SignUp
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
    }

  },
  computed: {
    ...mapState(["authentication", "forms"]),
  },
};
</script>

<style>
#logo-btn {
  max-height: 30px;
}
</style>
