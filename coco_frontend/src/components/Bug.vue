<template>
  <div>
    <v-card-title>Reporta un bug</v-card-title>
    <v-card-text>
      <v-textarea
        outlined
        name="input-7-4"
        v-model="description"
        label="Descripción"
      ></v-textarea>
      <v-file-input
      v-if="bug"
        accept="image/png, image/jpeg, image/bmp"
        append-icon="mdi-image-plus"
        label="Captura de pantalla"
        @change="addPhoto"
          ></v-file-input>
    </v-card-text>
    <v-card-actions class="px-4 pb-5">
      <v-btn text :disabled="loading" @click="$emit('closeBug')" color="error"
        >Cerrar</v-btn
      >
      <v-btn color="primary" @click="sendBug" :loading="loading">Enviar</v-btn>
    </v-card-actions>
    <v-snackbar v-model="snackbar">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Bug",
  data: () => ({
    description: "",
    img: "",
    apiDir: "bug/",
    snackbar: false,
    message: "",
    loading: false,
    bug: false
  }),
  computed: {
    ...mapState(["baseUrl"]),
  },
  methods: {
      addPhoto(img){
          this.img = img;
      },
    sendBug() {
      if (this.description) {
        this.loading = true;
        const formData = new FormData();
        formData.append("description", this.description);
        formData.append("img", this.img);
        let headers = {};
        delete headers["Content-Type"];
        fetch(this.baseUrl + this.apiDir, {
          method: "POST",
          headers: headers,
          body: formData,
        })
          .then((response) => {
            if (response.status == 200) {
              this.snackbar = true;
              this.message = "Bug reportado exitosamente!";
              this.description = "";
              this.$emit("closeBug");
            } else {
              throw new Error();
            }
          })
          .catch(() => {
            this.snackbar = true;
            this.message =
              "Ha sucedido un error inesperado. Intenta de nuevo más tarde.";
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
  },
};
</script>

<style >
.v-input__prepend-outer{
    z-index: -1;
}
</style>