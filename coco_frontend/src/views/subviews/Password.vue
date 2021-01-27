<template>
  <div>
    <v-container fluid>
      <div class="display-1">
        <v-btn
          @click="$router.push({ name: 'Account' })"
          class="mr-3"
          icon
          color="primary"
        >
          <v-icon> mdi-arrow-left </v-icon> </v-btn
        >Cambia tu contraseña
      </div>

      <v-divider></v-divider>
      <form @submit.prevent="resetPassword">
        <v-row align="center">
          <v-col cols="12" class="pb-0">
            <v-text-field
              v-model="oldPassword"
              label="Contraseña actual"
              :type="viewOld ? 'text' : 'password'"
              :append-icon="viewOld ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="viewOld = !viewOld"
            ></v-text-field>
          </v-col>
          <v-col cols="12" class="pb-0">
            <v-text-field
              v-model="newPassword"
              label="Nueva contraseña"
              :rules="[rules.required, passwordStrong]"
              :type="viewNew1 ? 'text' : 'password'"
              :append-icon="viewNew1 ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="viewNew1 = !viewNew1"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-text-field
              v-model="newPassword2"
              label="Confirme la contraseña"
              :rules="[rules.required, passwordsMatching]"
              :type="viewNew2 ? 'text' : 'password'"
              :append-icon="viewNew2 ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="viewNew2 = !viewNew2"
            ></v-text-field>
          </v-col>
          <v-btn
            class="ml-3"
            :loading="loading"
            :disabled="!(valid1 && valid2 && oldPassword.length) ? true : false"
            color="primary darken-3"
            type="submit"
            >Actualizar</v-btn
          >
        </v-row>
      </form>
    </v-container>
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
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Password",
  data: () => ({
    oldPassword: "",
    newPassword: "",
    newPassword2: "",
    apiDir: "user-auth/password/change/",
    rules: {
      required: (value) => !!value || "Obligatorio",
    },
    viewOld: false,
    viewNew1: false,
    viewNew2: false,
    valid1: false,
    valid2: false,
    loading: false,
    message: "",
    snackbar: false,
  }),
  computed: {
    ...mapState(["user", "authentication", "baseUrl"]),
    passwordStrong() {
      var regex = /^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$/;
      if (!regex.test(this.newPassword)) {
        this.valid2 = false;
        return "Contraseña débil";
      }
      if (this.newPassword == this.oldPassword) {
        this.valid2 = false;
        return "No puede ser igual a tu contraseña anterior";
      } else {
        this.valid2 = true;
        return true;
      }
    },
    passwordsMatching() {
      if (this.newPassword !== this.newPassword2) {
        this.valid1 = false;
        return "Las contraseñas no coinciden";
      } else {
        this.valid1 = true;
        return true;
      }
    },
  },
  methods: {
    resetPassword() {
      if (this.valid1 && this.valid2 && this.oldPassword) {
        this.loading = true;
        let formData = {
          old_password: this.oldPassword,
          new_password1: this.newPassword,
          new_password2: this.newPassword2,
        };
        fetch(this.baseUrl + this.apiDir, {
          method: "POST",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        })
          .then((response) => {
            if (response.ok) {
              this.snackbar = true;
              this.message = "Contraseña actualizada exitosamente";
              this.oldPassword = "";
              this.newPassword = "";
              this.newPassword2 = "";
            } else {
              throw new Error();
            }
          })
          .catch(() => {
            this.snackbar = true;
            this.message = "Tu contraseña actual no es correcta.";
          })
          .finally(() => (this.loading = false));
      } else {
        this.snackbar = true;
        this.message = "Debes digitar toda la información solicitada.";
      }
    },
  },
};
</script>

<style>
</style>