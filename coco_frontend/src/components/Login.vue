<template>
  <div>
    <v-snackbar v-model="snackbar">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
    <v-dialog v-model="loginDialog" max-width="600">
      <v-card>
        <v-card-title> Inicia sesión con </v-card-title>
        <v-card-text>
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
                <p class="forgot-password">¿Olvidaste tu contraseña?</p>
                <v-progress-linear
                  v-if="loading"
                  color="accent"
                  indeterminate
                  rounded
                  height="6"
                ></v-progress-linear>
                <v-btn class="mr-4" color="primary" block type="submit">
                  Iniciar sesión
                </v-btn>
              </form>
            </v-row>
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex";

export default {
  name: "Login",
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
      let form_data = {}
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
          this.setCookie("token", response.key, 60);

          this.updateAuthInfo(responseObj);
          this.$router.push({ name: "Home" });
        })
        .catch((error) => {
          this.password = "";
          this.snackbar = true;
          this.message = "Credenciales inválidas!";
        });

      this.loading = false;
    },
    setCookie(cname, cvalue, exdays) {
      var d = new Date();

      d.setTime(d.getTime() + exdays * 24 * 60 * 60 * 1000);
      var expires = "expires=" + d.toUTCString();

      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    },
  },
};
</script>