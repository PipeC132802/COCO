<template>
  <v-container fluid>
          
          <div class="display-1"><v-btn
            @click="$router.push({ name: 'Account' })"
            class="mr-3"
            icon
            color="primary"
          >
            <v-icon> mdi-arrow-left </v-icon>
          </v-btn>Desactiva tu cuenta</div>
          <v-divider></v-divider>
    <v-row>
      <v-col cols="12">
        <v-list>
          <v-list-item
            class="user-item"
            :to="{ name: 'Profile', params: { username: user.username } }"
            title="Ver perfil"
          >
            <v-list-item-avatar size="55" color="secondary">
              <v-img
                v-if="user.profile_picture"
                :src="user.profile_picture"
              ></v-img>
              <span class="white--text" v-else>{{
                user.name.slice(0, 1)
              }}</span>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title
                v-html="user.name"
                :title="user.name"
              ></v-list-item-title>
              <v-list-item-subtitle
                v-html="'@' + user.username"
                :title="'@' + user.username"
              ></v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <h3 class="mx-3 title--text">Esta acción desactivará tu cuenta</h3>
        <p class="mx-3">
          Al desactivar tu cuenta, ningún usuario de
          <span
            @click="$router.push({ name: 'AboutUs' })"
            class="primary--text link mx-1"
            >COCO</span
          >
          podrá encontrar tu @usuario, nombre ni tus publicaciones.
        </p>
        <p class="mx-3">
          Para reactivar la cuenta simplemente debes iniciar sesión. Ten en
          cuenta que después de 30 días de haber desactivado tu cuenta no podrás
          recuperarla.
        </p>
        <v-btn outlined @click="dialog = true" block color="error">Desactivar</v-btn>
      </v-col>
    </v-row>
    <v-dialog v-model="dialog" max-width="500">
      <v-card class="pa-5">
        <v-row justify="center">

        <v-card-title class="text-center"> ¿Estás segur@? 🥺 </v-card-title>
        </v-row>
        <v-card-actions>
          <v-row justify="center">

          <v-btn
            :loading="loading"
            @click="deactivateAccount"
            text
            color="error"
            class="mx-1"
          >
            Desactivar
          </v-btn>
          <v-btn @click="dialog = false" color="primary">
            Seguir usando COCO
          </v-btn>
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { removeCookie } from "@/js/cookiesfunctions.js";

export default {
  name: "DeactivateAccount",
  data: () => ({
    apiDir: "user-account-deactivated/",
    logOutApi: "user-auth/logout/",
    dialog: false,
    loading: false,
  }),
  computed: {
    ...mapState(["user", "authentication", "baseUrl"]),
  },
  methods: {
    ...mapMutations(["updateAuthInfo"]),
    deactivateAccount() {
      this.loading = true;
      fetch(this.baseUrl + this.apiDir, {
        method: "PUT",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status == 200) {
            this.deleteToken();
            this.closeSession();
          } else {
            throw new Error();
          }
        })
        .catch((err) => (this.loading = false));
    },
    closeSession() {
      let authObj = {
        accessToken: null,
        userIsAuthenticated: false,
      };
      //this.deleteToken(); This unauthenticate all users
      removeCookie("token");
      this.updateAuthInfo(authObj);
      this.$router.push({ name: "Welcome" });
    },
    deleteToken() {
      fetch(this.baseUrl + this.logOutApi, {
        method: "POST",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      });
    },
  },
};
</script>

<style>
.user-item:hover {
  background: rgb(202, 202, 202);
  border-radius: 10px;
}
.link:hover {
  cursor: pointer;
}
</style>