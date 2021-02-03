<template>
  <div>
    <v-dialog persistent v-model="signUpDialog" dense max-width="600">
      <v-card id="v-dialog">
        <v-card-title class="pl-8 pt-5 pb-0 mx-auto">
          <div class="mx-auto">Regístrate con</div>
        </v-card-title>
        <SocialLogin />
        <v-card-text class="pt-0 mt-0 pb-0">
          <div class="text-left pl-3 pt-2 pb-0 mb-0">
            <p class="ma-0">O ingresando tus datos</p>
          </div>
          <v-container class="pt-0">
            <form style="width: 100%" @submit.prevent="signUpSubmit">
              <v-row align="center">
                <v-col class="pt-0 pb-0" cols="12" md="6">
                  <v-text-field
                    class="mb-1"
                    v-model="firstName"
                    label="Nombres"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                </v-col>
                <v-col class="pb-0 pt-0" cols="12" sm="12" md="6">
                  <v-text-field
                    required
                    class="mb-1"
                    v-model="lastName"
                    label="Apellidos"
                    :rules="[rules.required]"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-text-field
                required
                class="mb-1 pt-0"
                v-model="username"
                label="Usuario"
                :rules="[rules.required, rules.valid]"
              ></v-text-field>
              <v-text-field
                required
                class="mb-1 pt-1"
                type="email"
                v-model="email"
                label="Correo"
                :rules="[rules.required]"
              ></v-text-field>
              <v-row align="center">
                <v-col class="pt-0 pb-0" cols="12" sm="12" md="6">
                  <v-text-field
                    required
                    class="mb-1 pt-0"
                    v-model="password1"
                    label="Contraseña"
                    :type="view1 ? 'text' : 'password'"
                    :rules="[rules.required, passwordStrong]"
                    :append-icon="view1 ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="view1 = !view1"
                  ></v-text-field>
                </v-col>
                <v-col class="pt-0 pb-0" cols="12" sm="12" md="6">
                  <v-text-field
                    required
                    class="mb-1 pt-0 pb-0"
                    v-model="password2"
                    label="Repita la contraseña"
                    :type="view2 ? 'text' : 'password'"
                    :rules="[rules.required, passwordsMatching]"
                    :append-icon="view2 ? 'mdi-eye' : 'mdi-eye-off'"
                    @click:append="view2 = !view2"
                  ></v-text-field>
                </v-col>
              </v-row>

              <p class="forgot-password">¿Olvidaste tu contraseña?</p>
              <v-progress-linear
                v-if="loading"
                color="accent"
                indeterminate
                rounded
                height="6"
              ></v-progress-linear>
              <v-btn
                class="mr-4"
                color="primary"
                :loading="loading"
                block
                type="submit"
              >
                Registrate
              </v-btn>
            </form>
          </v-container>
          <p align="center">
            ¿Ya tienes una cuenta?
            <a @click="updateFormsDialog(true, false)">Inicia sesión</a>
          </p>
        </v-card-text>
        <v-card-actions class="mt-0 pt-0 mr-3">
          <v-spacer></v-spacer>
          <v-btn color="error" @click="signUpDialog = false" text>
            cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
      <v-snackbar v-model="snackbar">
        {{ message }}
        <template v-slot:action="{ attrs }">
          <v-btn
            color="error darken-1"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
            Cerrar
          </v-btn>
        </template>
      </v-snackbar>
    </v-dialog>
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex";
import { setCookie } from "@/js/cookiesfunctions.js";
import SocialLogin from "../components/SocialLogin.vue";
export default {
  name: "SignUp",
  components: {
    SocialLogin,
  },
  data: () => ({
    firstName: "",
    lastName: "",
    username: "",
    email: "",
    password1: "",
    password2: "",
    signUpDialog: false,
    rules: {
      required: (value) => !!value || "Obligatorio",
      valid: (value) =>
        !/^(?=[a-zA-Z0-9._]{4,20}$)(?!.*[_.]{2})[^_.].*[^_.]$/.test(value)
          ? "Nombre de usuario inválido"
          : true,
    },
    view1: false,
    view2: false,
    loading: false,
    valid: false,
    valid2: false,
    apiDir: "create-user/",
    snackbar: false,
    message: "",
  }),
  created() {
    this.signUpDialog = this.forms.signUpDialog;
  },
  beforeUpdate() {
    let formDialog = {
      loginDialog: false,
      signUpDialog: this.signUpDialog,
    };
    this.updateFormsInfo(formDialog);
  },
  computed: {
    ...mapState(["forms", "baseUrl"]),

    passwordStrong() {
      var regex = /^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$/;
      if (!regex.test(this.password1)) {
        this.valid2 = false;
        return "Contraseña débil";
      } else {
        this.valid2 = true;
        return true;
      }
    },
    passwordsMatching() {
      if (this.password1 !== this.password2) {
        this.valid = false;
        return "Las contraseñas no coinciden";
      } else {
        this.valid = true;
        return true;
      }
    },
  },
  methods: {
    ...mapMutations(["updateFormsInfo", "updateAuthInfo"]),
    signUpSubmit() {
      this.loading = true;
      if (this.valid && this.valid2) {
        let formData = {
          first_name: this.firstName,
          last_name: this.lastName,
          username: this.username,
          email: this.email,
          password: this.password1,
        };
        this.createUser(formData);
      } else {
      }
    },
    createUser(FormData) {
      fetch(this.baseUrl + this.apiDir, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(FormData),
      })
        .then((response) => {
          if (response.status != 200) {
            throw new Error();
          } else {
            return response.json();
          }
        })
        .then((response) => {
          let responseObj = {
            accessToken: response.key,
            userIsAuthenticated: !!response.key,
          };
          setCookie("token", response.key, 60);
          this.updateAuthInfo(responseObj);
        })
        .catch((e) => {
          this.snackbar = true;
          this.message =
            "Ya existe una cuenta con este nombre de usuario o correo";
        })
        .finally(() => {
          this.signUpDialog = false;
          this.loading = false;

          this.$router.push({ name: "MoreInfo" });
        });
    },
    updateFormsDialog(login, signup) {
      let formDialog = {
        loginDialog: login,
        signUpDialog: signup,
      };

      this.updateFormsInfo(formDialog);
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