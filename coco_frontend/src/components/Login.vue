<template>
  <div>
    <v-dialog persistent v-model="loginDialog" max-width="600">
      <v-card id="v-dialog">
        <v-card-title class="pb-0 mb-0"> <div class="mx-auto">Inicia sesión con</div> </v-card-title>
        <SocialLogin />
        <v-card-text class="pb-0 mb-0">
                  <div class="text-left pl-0 pt-2 pb-0 mb-0"><p class="ma-0">O ingresando tus datos</p></div>

          <v-container fluid>
            <v-row>
              <form style="width: 100%" @submit.prevent="loginSubmit">
                <v-text-field
                  class="mb-1"
                  v-model="username"
                  label="Usuario o correo"
                  :rules="[rules.required]"
                ></v-text-field>
                <v-text-field
                  class="mb-1"
                  v-model="password"
                  label="Contraseña"
                  :type="view ? 'text' : 'password'"
                  :rules="[rules.required]"
                  :append-icon="view ? 'mdi-eye' : 'mdi-eye-off'"
                  @click:append="view = !view"
                ></v-text-field>

                <v-progress-linear
                  v-if="loading"
                  color="accent"
                  indeterminate
                  rounded
                  height="6"
                ></v-progress-linear>
                <v-btn class="mr-4 mb-2" color="primary" block type="submit">
                  Iniciar sesión
                </v-btn>
                <a>¿Olvidaste tu contraseña?</a>
              </form>
            </v-row>
          </v-container>
          <p align="center">
            ¿No tienes una cuenta?
            <a @click="updateFormsDialog(false, true)">Regístrate gratis</a>
          </p>
        </v-card-text>
        <v-card-actions class="pt-0 mr-4 mb-2">
          <v-spacer></v-spacer>
          <v-btn color="error" @click="loginDialog = false" text>
            cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-snackbar v-model="snackbar">
        {{ message }}
        <template v-slot:action="{ attrs }">
          <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
            Cerrar
          </v-btn>
        </template>
      </v-snackbar>
    </v-dialog>

    <ResetPassword v-if="resetPassword" v-on:dialog-state="changeDialogState" />
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import { setCookie } from "@/js/cookiesfunctions.js";
import ResetPassword from "@/components/subcomponents/ResetPassword.vue";
import SocialLogin from "../components/SocialLogin.vue";
export default {
  name: "Login",
  components: {
    ResetPassword,
    SocialLogin,
  },
  data: () => ({
    username: "",
    password: "",
    apiDir: "user-auth/login/",
    loading: false,
    incorrectAuth: false,
    snackbar: false,
    message: "",
    loginDialog: false,
    view: false,
    resetPassword: false,
    rules: {
      required: (value) => !!value || "Obligatorio",
    },
  }),
  created() {
    this.loginDialog = this.forms.loginDialog;
  },
  beforeUpdate() {
    let formDialog = {
      loginDialog: this.loginDialog,
      signUpDialog: false,
    };
    this.updateFormsInfo(formDialog);
  },
  computed: {
    ...mapState(["forms", "baseUrl"]),
  },
  methods: {
    ...mapMutations(["updateFormsInfo", "updateAuthInfo"]),
    loginSubmit() {
      this.loading = true;
      let form_data = {};
      if (this.username.indexOf("@") > -1) {
        form_data = {
          username: "",
          email: this.username,
          password: this.password,
        };
      } else {
        form_data = {
          username: this.username,
          email: "",
          password: this.password,
        };
      }

      fetch(this.baseUrl + this.apiDir, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "content-type": "application/json",
        },
        body: JSON.stringify(form_data),
      })
        .then((response) => {
          if (response.status != 200) {
            throw new Error();
          }
          return response.json();
        })

        .then((response) => {
          let responseObj = {
            accessToken: response.key,
            userIsAuthenticated: !!response.key,
          };
          setCookie("token", response.key, 60);

          this.updateAuthInfo(responseObj);
          this.updateFormsDialog(false, false);
          this.$router.push({ name: "Home" });
        })
        .catch(() => {
          this.password = "";
          this.snackbar = true;
          this.message = "Credenciales inválidas!";
        })
        .finally(() => {
          this.loading = false;
        });
    },
    updateFormsDialog(login, signup) {
      let formDialog = {
        loginDialog: login,
        signUpDialog: signup,
      };

      this.updateFormsInfo(formDialog);
    },
    changeDialogState: function (dialogState) {
      this.resetPassword = dialogState;
    },
  },
};
</script>

<style scoped>
#v-dialog {
  overflow-x: hidden;
}
p,
a {
  font-size: 12pt;
}
a {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>