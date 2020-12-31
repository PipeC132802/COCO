<template>
  <div>
    <v-card elevation="3" width="100%">
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
      <v-form @submit.prevent="createBarter">
        <v-card class="px-5">
          <v-card-title class="mb-0 pb-0"> Nuevo Trueque </v-card-title>
          <v-card-text class="ma-0 pt-0 pb-0">
            <v-container class="pa-0">
              <v-row class="pa-0">
                <v-col cols="12">
                  <v-text-field
                    v-model="title"
                    label="Título"
                    required
                    :rules="[rules.required, rules.maxLength]"
                    counter="255"
                  ></v-text-field>
                </v-col>
                <v-col class="pt-0" cols="12">
                  <v-textarea
                    class="pt-0 mt-0"
                    auto-grow
                    label="Descripción"
                    v-model="description"
                    required
                    :rules="[rules.required]"
                  ></v-textarea>
                </v-col>
                <v-col class="pt-0 mt-0" cols="12" sm="6">
                  <Area v-on:skill="setSkill" :subject="'skill'" />
                </v-col>
                <v-col class="pt-0 mt-0" cols="12" sm="6">
                  <Area v-on:interest="setInterest" :subject="'interest'" />
                </v-col>
                <v-col>
                  <v-autocomplete
                    v-model="country"
                    :items="countriesList"
                    hide-no-data
                    hide-selected
                    item-text="nombre"
                    item-value="nombre"
                    label="País"
                    return-object
                    :rules="[rules.required]"
                    required
                    class="pa-0"
                  >
                    <template v-slot:item="data">
                      <template v-if="typeof data.item !== 'object'">
                        <v-list-item-content
                          v-text="data.item"
                        ></v-list-item-content>
                      </template>
                      <template v-else>
                        <v-list-item-avatar>
                          <img
                            v-if="data.item.iso2 != 'AN'"
                            width="30"
                            :alt="data.item.iso2"
                            :src="`https://flagcdn.com/${data.item.iso2.toLowerCase()}.svg`"
                          />
                          <img
                            v-else
                            alt="ANT"
                            width="30"
                            src="https://upload.wikimedia.org/wikipedia/commons/a/ae/Flag_of_the_Netherlands_Antilles_%281986%E2%80%932010%29.svg"
                          />
                        </v-list-item-avatar>
                        <v-list-item-content>
                          <v-list-item-title
                            v-if="data.item.iso2 != 'AN'"
                            v-html="`(${data.item.iso2}) ${data.item.nombre}`"
                          ></v-list-item-title>
                          <v-list-item-title
                            v-else
                            v-html="`(ANT) ${data.item.nombre}`"
                          ></v-list-item-title>
                        </v-list-item-content>
                      </template>
                    </template>
                  </v-autocomplete>
                </v-col>
                <v-col>
                  <v-text-field
                    class="pa-0"
                    v-model="city"
                    label="Ciudad"
                    :rules="[rules.required]"
                    required
                  ></v-text-field>
                </v-col>
                <v-col class="pt-0" sm="12">
                  <v-select
                    required
                    :items="items"
                    v-model="mode"
                    label="Modalidad"
                    :rules="[rules.required]"
                  ></v-select>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions class="pr-4 mt-0 pb-5">
            <v-spacer></v-spacer>
            <v-btn color="error" @click="dialog = false" text> Cancelar </v-btn>
            <v-btn :loading="loading" type="submit" color="primary darken-2">
              Publicar
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-dialog>
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
import countries from "@/json/countriescodes.json";
import Area from "../components/subcomponents/Area.vue";
export default {
  name: "NewBarter",
  components: {
    Area,
  },
  data() {
    return {
      title: "",
      description: "",
      skill: "",
      interest: "",
      country: "",
      city: "",
      mode: "",
      dialog: false,
      loading: false,
      snackbar: false,
      message: "",
      apiDir: "barter-api/",
      items: [
        { value: 1, text: "Presencial" },
        { value: 2, text: "Virtual" },
      ],
      
      rules: {
        required: (value) => !!value || "Obligatorio",
        maxLength: v => v.length <= 255 || 'Max. 255 caracteres'
      },
    };
  },
  beforeUpdate() {},
  computed: {
    ...mapState(["user", "authentication", "baseUrl"]),
    countriesList() {
      return countries.map((country) => {
        return country;
      });
    },
  },
  methods: {
    createBarter() {
      if (
        this.title &&
        this.description &&
        this.skill &&
        this.interest &&
        this.country &&
        this.city &&
        this.mode
      ) {
        let formData = {
          title: this.title,
          description: this.description,
          country: this.country.nombre,
          city: this.city,
          skill: this.skill,
          interest: this.interest,
          mode: this.mode,
        };
        fetch(this.baseUrl + this.apiDir, {
          method: "POST",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(formData)
        })
        .then((response)=>(response.json()))
        .then((response)=>{
          this.clearFields();
          
          this.$emit('newBarterPosted')
        })
      } else {
        this.snackbar = true;
        this.message = "Debes ingresar toda la información solicitada!";
      }
    },
    setSkill(skill) {
      this.skill = skill;
    },
    setInterest(interest) {
      this.interest = interest;
    },
    clearFields(){
      this.country = '';
      this.city = '';
      this.mode = '';
      this.title = '';
      this.description = '';
      this.skill = '';
      this.interest = '';
      this.dialog = false;
    }
  },
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