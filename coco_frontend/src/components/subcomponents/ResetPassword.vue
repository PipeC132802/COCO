<template>
  <div>
    <v-dialog max-width="600" v-model="resetPassword">
      <v-card>
        <v-card-title class="pb-0"> Reestablece tu contraseña </v-card-title>
        <v-card-text>
          <form class="mb-4" action="">
            <v-text-field
              required
              type="email"
              v-model="email"
              label="Correo"
            ></v-text-field>
            <v-btn class="mr-4 mb-2" color="primary" block type="submit">
              Recuperar contraseña
            </v-btn>
          </form>
          <p align="center">
            ¿No tienes cuenta en COCO?
            <a @click="updateFormsDialog(false,true)"> Regístrarse </a>
          </p>
          <p align="center">
            También puedes
            <a @click="updateFormsDialog(true,false)"> Iniciar sesión </a>
          </p>
        </v-card-text>
        <v-card-actions class="pt-0 mr-4">
          <v-spacer></v-spacer>
          <v-btn color="error" @click="resetPassword = false" text>
            cerrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import {mapMutations} from "vuex";
export default {
  name: "ResetPassword",
  data: () => ({
    resetPassword: true,
    email: "",
  }),
  beforeUpdate() {
    this.$emit("dialog-state", this.resetPassword);
  },
  computed:{
     
  },
  methods:{
       ...mapMutations(["updateFormsInfo"]),
      updateFormsDialog(login, signup) {
      let formDialog = {
        loginDialog: login,
        signUpDialog: signup,
      };
      this.resetPassword = false;
      this.updateFormsInfo(formDialog);
    },
  }
};
</script>
<style scoped>
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