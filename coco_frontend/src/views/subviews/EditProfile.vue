<template>
  <div class="mx-3">
    <v-card elevation="3" class="px-3">
      <v-card-title>
        <v-btn
          icon
          color="primary"
          class="mr-3"
          exact
          :to="{ name: 'Profile', props: { username: $route.params.username } }"
          ><v-icon>mdi-arrow-left-thick</v-icon></v-btn
        >
        Editar tu información
      </v-card-title>
    </v-card>
    <v-card elevation="3" class="mt-3 px-3">
      <v-card-title class="mb-0">
        Información del perfil
        <v-container class="header ma-0 pa-0"></v-container>
      </v-card-title>
      <v-card-text class="mb-5">
        <v-form
          ref="form"
          v-model="valid"
          @submit.prevent="updateUserInfo"
          lazy-validation
        >
          <v-text-field
            class="mb-1"
            v-model="username"
            label="Nombre de usuario"
            required
          ></v-text-field>
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
          <Contact :contactObj="contactObj" v-on:contact="contactInfo" />
          <v-textarea
            v-model="bio"
            placeholder="Soy una persona amante de los libros..."
            auto-grow
            class="mt-0 pt-0"
            label="Bio"
          ></v-textarea>
          <Areas v-on:skills="skillsInfo" :areas="skills" subject="skills" />
          <Areas v-on:learn="learnInfo" :areas="interests" subject="learn" />
          <small>
            * Las Habilidades y los intereses están ocultos. Si deseas verlos,
            ubícate en dichos campos y presiona la tecla espacio.
          </small>
          <v-card-actions class="pr-0">
            <v-btn
              :loading="loading"
              color="primary darken-3"
              class="ml-auto"
              type="submit"
            >
              Guardar
            </v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
    </v-card>
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
import Contact from "@/components/subcomponents/Contact.vue";
import Areas from "@/components/subcomponents/Areas.vue";
import { mapMutations, mapState } from "vuex";
export default {
  components: {
    Contact,
    Areas,
  },
  data: () => ({
    apiDir: "user-info-update/",
    valid: false,
    username: "",
    firstName: "",
    lastName: "",
    bio: "",
    contactObj: {
      country: "",
      city: "",
      cellphone: "",
      prefix: "",
    },
    skills: [],
    interests: [],
    formData: {},
    loading: false,
    snackbar: false,
    message: "",
  }),
  computed: {
    ...mapState(["baseUrl", "user", "authentication"]),
  },
  beforeUpdate() {
    this.formData.username = this.username;
    this.formData.first_name = this.firstName;
    this.formData.last_name = this.lastName;
    this.formData.bio = this.bio;
  },
  mounted() {
    if(!this.user){
      this.$router.push({name: "Welcome"})
    }
    this.retrieveUserInfo();
  },
  methods: {
    ...mapMutations(["setUser"]),
    retrieveUserInfo() {
      fetch(this.baseUrl + this.apiDir, {
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.username = response.username;
          this.firstName = response.first_name;
          this.lastName = response.last_name;
          this.bio = response.bio;
          this.contactObj.country = response.country;
          this.contactObj.city = response.city;
          this.contactObj.prefix = response.prefix;
          this.contactObj.cellphone = response.cellphone;
          this.skills = response.skills;
          this.interests = response.interests;
          this.formData.skills = response.skills;
          this.formData.interests = response.interests;
        });
    },
    updateUserInfo() {
      this.loading = true;
      if (!this.formData.skills.length) {
        this.snackbar = true;
        this.message = "Debes agregar habilidades!";
        this.loading = false;
      } else if (!this.formData.interests.length) {
        this.snackbar = true;
        this.message = "Debes agregar intereses!";
        this.loading = false;
      } else {
        fetch(this.baseUrl + this.apiDir, {
          method: "PUT",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.formData),
        })
          .then((response) => {
            if (response.status == 200) {
              this.$root.$emit("userInfoUpdated")
              this.snackbar = true;
              this.message = "Información actualizada exitosamente!";
            } else {
              throw new Error();
            }
          })
          .then((response) => {
            let user = this.user;
            user.username = this.username;
            this.name = this.firstName + " " + this.lastName;
            this.setUser(user);
            this.$router.push({
              name: "Profile",
              params: { username: this.username },
            });
          })
          .catch((err) => {
            this.snackbar = true;
            this.message = "Ha sucedido un error. Intenta de nuevo más tarde.";
          })
          .finally(() => {
            this.loading = false;
          });
      }
    },
    contactInfo(contactObj) {
      this.formData.country = contactObj.country;
      this.formData.city = contactObj.city;
      this.formData.cellphone = contactObj.phone;
    },
    learnInfo(interests) {
      this.formData.interests = interests;
    },
    skillsInfo(skills) {
      this.formData.skills = skills;
    },
  },
};
</script>

<style scoped>
.header {
  border-bottom: 3px solid #09243d;
}
</style>