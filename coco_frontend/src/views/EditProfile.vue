<template>
  <div>
    <v-card elevation="3">
      <v-card-title>
        <v-btn
          icon
          color="primary"
          class="mr-3"
          exact
          :to="{ name: 'Profile', props: { username: $route.params.username } }"
          ><v-icon>mdi-arrow-left-thick</v-icon></v-btn
        >
        Editar información de tu cuenta
      </v-card-title>
    </v-card >
    <v-card elevation="12" class="mt-3">
      <v-card-title class="mb-0">
        Información del perfil
        <v-container class="header ma-0 pa-0"></v-container>
      </v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid" lazy-validation>
          <v-row class="ma-0 pa-0">
            <v-col xs="12" md="6" class="pl-0">
              <v-text-field
                class="mb-1"  
                v-model="firstName"
                label="Nombres"
                required
              ></v-text-field>
            </v-col>
            <v-col sm="12" md="6" class="px-0">
              <v-text-field
                required
                class="mb-1"
                v-model="lastName"
                label="Apellidos"
              ></v-text-field>
            </v-col>
          </v-row>
          <Contact v-on:contact="contactInfo" />
          <v-textarea
            v-model="bio"
            placeholder="Soy una persona amante de los libros..."
            auto-grow
            class="mt-0 pt-0"
            label="Bio"
          ></v-textarea>
          <Areas v-on:skills="skillsInfo" subject="skills" />
          <Areas v-on:learn="learnInfo" subject="learn" />
          <v-card-actions class="pr-0">
            <v-btn color="primary darken-3" class="ml-auto" @click="validate">
              Guardar
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import Contact from "@/components/subcomponents/Contact.vue";
import Areas from "@/components/subcomponents/Areas.vue";
export default {
  components: {
    Contact,
    Areas
  },
};
</script>

<style>
.header {
  border-bottom: 3px solid #09243d;
}
</style>