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
    </v-card>
    <v-card elevation="12" class="mt-3">
      <v-card-title class="mb-0">
        Información del perfil
        <v-container class="header ma-0 pa-0"></v-container>
      </v-card-title>
      <v-card-text>
        <v-form
          ref="form"
          v-model="valid"
          @submit.prevent="updateUserInfo"
          lazy-validation
        >
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
          <Areas
            v-on:skills="skillsInfo"
            :areas="skills"
            subject="skills"
          />
          <Areas
            v-on:learn="learnInfo"
            :areas="interests"
            subject="learn"
          />
          <small>
            * Las Habilidades y los intereses están ocultos. Si deseas verlos,
            ubícate en dichos campos y presiona la tecla espacio.
          </small>
          <v-card-actions class="pr-0">
            <v-btn color="primary darken-3" class="ml-auto" type="submit">
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
import { mapMutations, mapState } from "vuex";
export default {
  components: {
    Contact,
    Areas,
  },
  data: () => ({
    apiDir: "user-info-update/",
    valid: false,
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
  }),
  computed: {
    ...mapState(["baseUrl", "user", "authentication"]),
  },
  beforeUpdate() {},
  created() {
    this.retrieveUserInfo();
  },
  methods: {
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
          this.firstName = response.first_name;
          this.lastName = response.last_name;
          this.bio = response.bio;
          this.contactObj.country = response.country;
          this.contactObj.city = response.city;
          this.contactObj.prefix = response.prefix;
          this.contactObj.cellphone = response.cellphone;
          this.skills = response.skills;
          this.interests = response.interests;
        });
    },
    contactInfo(contactObj) {
      this.contactObj = contactObj;
    },
    skillsInfo(skillsObj) {
      this.skills = skillsObj;
    },
    learnInfo(interestsObj) {
      this.interests = interestsObj;
    },
    updateUserInfo(){
      let formData = {
        first_name: this.firstName,
        last_name: this.lastName,
        country: this.contactObj.country,
        city: this.contactObj.city,
        cellphone: this.contactObj.phone,
        bio: this.bio,
        skills: this.skills,
        interests: this.interests
      }
      fetch(this.baseUrl+this.apiDir,{
        method: 'PUT',
        headers:{
          Authorization: `Token ${this.authentication.accessToken}`,
        },
        body: JSON.stringify(formData)
      })
      .then((response)=>{return response.json()})
      .then((response)=>{
        console.log(response)
      })
      .catch((err)=>{console.error(err)})
    }
  },
};
</script>

<style>
.header {
  border-bottom: 3px solid #09243d;
}
</style>