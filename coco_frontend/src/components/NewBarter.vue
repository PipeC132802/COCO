<template>
  <div>
    <v-card elevation="4" width="100%">
      <v-card-title>
        <v-row dense>
          <v-avatar class="mt-1" color="secondary">
            <img
              v-if="user.profile_picture"
              :src="user.profile_picture"
              :alt="user.name"
            />
            <span v-else-if="user.name" class="white--text">{{
              user.name.slice(0, 1)
            }}</span>
          </v-avatar>
          <v-col>
            <input
              @click="dialog = true"
              class="ml-2"
              type="text"
              :placeholder="`¿Quieres aprender algo nuevo, ${user.name}?`"
            />
          </v-col>
        </v-row>
      </v-card-title>
      <v-divider class="mx-3"></v-divider>
      <v-card-actions>
        <v-btn @click="dialog = true" rounded text color="secondary">
          <v-icon left>mdi-school</v-icon>
          Quiero aprender
        </v-btn>
        <v-btn @click="dialog = true" rounded text color="secondary">
          <v-icon left>mdi-teach</v-icon>
          Voy a enseñar
        </v-btn>
        <v-btn @click="dialog = true" class="ml-auto" color="primary darken-2">
          Publicar
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-dialog v-if="dialog" v-model="dialog" persistent max-width="600px">
      <v-card>
        <v-card-title class="p b-0">
          <h3 class="ml-2 headline">Nuevo Trueque</h3>
        </v-card-title>
        <v-card-text >
          <v-container>
            <v-row>
              <v-col cols="12"> 
                <v-text-field label="Título" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea auto-grow label="Descripción"></v-textarea>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  :items="['0-17', '18-29', '30-54', '54+']"
                  label="Área que me desempeño"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  :items="['0-17', '18-29', '30-54', '54+']"
                  label="Área que deseo aprender"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field label="Pais" required></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="Estado"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  label="Ciudad"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          <small class="ml-2">Todos los campos son obligatorios</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="dialog = false" text> Cancelar </v-btn>
          <v-btn color="primary darken-2" @click="dialog = false"> Publicar </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "NewBarter",
  data: () => ({
    dialog: false,
  }),
  computed: {
    ...mapState(["user"]),
  },
  created(){
      let formdata = {
          username: 'pipe',
          password: 'Coco_F132802'
      }
     
  }
};
</script>

<style scoped>
input {
  outline: none;
  width: 100%;
  background: #f3f3f3;
  padding: 10px 20px;
  border-radius: 50px;
}
</style>