<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col sm="10">
        <v-stepper v-model="e1">
          <v-stepper-header>
            <v-stepper-step :complete="e1 > 1" step="1">
              Personal
            </v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step :complete="e1 > 2" step="2">
              Sobre ti
            </v-stepper-step>

            <v-divider></v-divider>

            <v-stepper-step step="3">Foto de perfil </v-stepper-step>
          </v-stepper-header>

          <v-stepper-items>
            <v-stepper-content step="1">
              <v-card class="ma-0 pa-0">
                <v-container class="pa-0" fluid>
                  <v-row justify="center" class="pa-0" wrap>
                    <v-col sm="12" md="10" lg="8">
                      <form @submit.prevent="signUpSubmit">
                        <v-row class="pa-0">
                          <v-col class="ma-0" xs="12" md="12">
                            <Contact v-on:contact="contactInfo" />
                            <Personal v-on:about="aboutInfo" />
                          </v-col>
                        </v-row>
                        <v-card-actions class="pa-0">
                          <v-spacer></v-spacer>
                          <v-btn
                            color="primary"
                            :loading="loadingBtn"
                            @click="submitContact"
                          >
                            Guardar
                          </v-btn>
                        </v-card-actions>
                      </form>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card>
            </v-stepper-content>
            <v-stepper-content step="2">
              <v-container class="pa-0" fluid>
                <v-row justify="center" class="pa-0" wrap>
                  <v-col sm="12" md="10" lg="8">
                    <form @submit.prevent="signUpSubmit">
                      <v-row class="pa-0">
                        <v-col class="ma-0" xs="12" md="12">
                          <Areas v-on:skills="skillsInfo" subject="skills" />
                          <Areas v-on:learn="learnInfo" subject="learn" />
                          <v-textarea
                            v-model="bio"
                            placeholder="Soy una persona amante de los libros..."
                            auto-grow
                            label="Bio"
                          ></v-textarea>
                        </v-col>
                      </v-row>
                    </form>
                    <v-card-actions class="pa-0">
                      <v-spacer></v-spacer>
                      <v-btn
                        color="primary"
                        :loading="loadingBtn"
                        @click="submitAbout"
                      >
                        Guardar
                      </v-btn>
                    </v-card-actions>
                  </v-col>
                </v-row>
              </v-container>
            </v-stepper-content>

            <v-stepper-content step="3">
              <v-container class="pa-0" fluid>
                <v-row justify="center" class="pa-0" wrap>
                  <v-col sm="12" md="10" lg="8">
                    <form @submit.prevent="signUpSubmit">
                      <v-row class="pa-0">
                        <v-col class="ma-0" xs="12" md="12">
                          <ProfilePicture subject="skills" />
                        </v-col>
                      </v-row>
                    </form>
                    <v-card-actions class="pa-0">
                      <v-spacer></v-spacer>
                      <v-btn
                        class="mr-2"
                        outlined
                        color="primary darken-2"
                        @click="goHome"
                      >
                        Saltar
                      </v-btn>
                      <v-btn color="primary" @click="e1 = 1"> Continue </v-btn>
                    </v-card-actions>
                  </v-col>
                </v-row>
              </v-container>
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>


<script>
import Contact from "@/components/subcomponents/Contact.vue";
import Areas from "@/components/subcomponents/Areas.vue";
import Personal from "@/components/subcomponents/Personal.vue";
import ProfilePicture from "@/components/subcomponents/ProfilePicture.vue";
import { mapState } from "vuex";
export default {
  components: {
    Contact,
    Areas,
    Personal,
    ProfilePicture,
  },
  data() {
    return {
      contact: {
        country: "",
        city: "",
        phone: "",
      },
      about: {
        birthday: "",
        gender: "",
        bio: "",
      },
      areas: {
        skills: "",
        learn: "",
      },
      profilePicture: "",
      bio: "",
      snackbar: false,
      message: "",
      loadingBtn: false,
      apiDirs: {
        contact: "contact-user/",
        about: "about-user/",
      },
      e1: 1,
      rules: {
        required: (value) => !!value || "Obligatorio",
        valid: (value) =>
          !/^(?=[a-zA-Z0-9._]{4,20}$)(?!.*[_.]{2})[^_.].*[^_.]$/.test(value)
            ? "Nombre de usuario inválido"
            : true,
      },
    };
  },
  beforeUpdate() {
    if (this.bio.length) this.about.bio = this.bio;
  },
  computed: {
    ...mapState(["authentication", "baseUrl"]),
  },
  created() {},
  methods: {
    contactInfo(contactObj) {
      this.contact = contactObj;
    },
    aboutInfo(aboutObj) {
      this.about.birthday = aboutObj.birthday;
      this.about.gender = aboutObj.gender;
    },
    skillsInfo(skills) {
      this.areas.skills = skills;
    },
    learnInfo(learn) {
      this.areas.learn = learn;
    },
    goHome() {
      this.$router.push({ name: "Home" });
    },
    submitContact() {
      this.loadingBtn = true;
      if (
        this.contact.country.trim().length &&
        this.contact.city.trim().length &&
        this.about.birthday &&
        this.about.gender
      ) {
        let body = {
          country: this.contact.country.trim(),
          city: this.contact.city.trim(),
          phone_number: this.contact.phone.trim(),
        };
        this.api(this.apiDirs.contact, body);
        
      } else {
        this.snackbar = true;
        this.message = "Completa los campos";
        this.loadingBtn = false;
      }
    },
    submitAbout(){
      this.loadingBtn = true;
      if (
        this.about.bio.trim().length &&
        this.areas.skills.length &&
        this.areas.learn.length
      ) {
        let body = {
          birthday: this.about.birthday.trim(),
          gender: this.about.gender.trim(),
          bio: this.about.bio.trim(),
          skills: this.areas.skills,
          learn: this.areas.learn,
        };
        
        this.api(this.apiDirs.about, body);
        
      } else {
        this.snackbar = true;
        this.message = "Completa los campos";
      }

    },
    api(url, body) {
      let headers = {
          Authorization: `Token ${this.authentication.accessToken}`,
          "Content-Type": "application/json",
        };
      fetch(this.baseUrl + url, {
        method: "POST",
        credentials: "same-origin",
        headers: headers,
        body: JSON.stringify(body),
      })
        .then((response) => response.json())
        .then((response) => {
          console.log(response);
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          this.loadingBtn = false
          if(this.e1<3){
            this.e1 += 1;
          } else{
            this.goHome();
          }
        }
        );
    },
  },
};
</script>