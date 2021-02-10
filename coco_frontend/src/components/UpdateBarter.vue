<template>
  <div>
    <v-form @submit.prevent="updateBarter">
      <v-card class="px-5">
        <v-card-title class="mb-0 pb-0"> Edita tu trueque </v-card-title>
        <v-card-text class="ma-0 pt-0 pb-0">
          <v-container class="pa-0">
            <v-row class="pa-0">
              <v-col cols="12">
                <v-text-field
                  v-model="titleModel"
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
                  v-model="descriptionModel"
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
                  v-model="cityModel"
                  label="Ciudad"
                  :rules="[rules.required]"
                  required
                ></v-text-field>
              </v-col>
              <v-col class="pt-0" sm="12">
                <v-select
                  required
                  :items="items"
                  v-model="modeModel"
                  label="Modalidad"
                  :rules="[rules.required]"
                ></v-select>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions class="pr-4 mt-0 pb-5">
          <v-spacer></v-spacer>
          <v-btn :disabled="loading" text @click="$emit('closeEditBarter')" color="error">Cerrar</v-btn>
          <v-btn :loading="loading" type="submit" color="primary darken-2">
            Editar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
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
  props: ["barter"],
  data() {
    return {
      loading: false,
      snackbar: false,
      title: "",
      description: "",
      country: {
        nombre: "",
      },
      city: "",
      message: "",
      skill: "",
      interest: "",
      mode: "",
      apiDir: "barter/",
      items: [
        { value: 1, text: "Presencial" },
        { value: 2, text: "Virtual" },
      ],
      rules: {
        required: (value) => !!value || "Obligatorio",
        maxLength: (v) => v.length <= 255 || "Max. 255 caracteres",
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
    titleModel: {
      get: function () {
        this.title = this.barter.title;
        return this.barter.title;
      },
      set: function (title) {
        this.title = title;
      },
    },
    countryModel: {
      get: function () {
        this.country = this.barter.about.place.split(",")[1] ;
        return  this.barter.about.place.split(",")[1] ;
      },
      set: function (country) {
        this.country = country;
      },
    },
    cityModel: {
      get: function () {
        this.city = this.barter.about.place.split(",")[0];
        return this.barter.about.place.split(",")[0];
      },
      set: function (city) {
        this.city = city;
      },
    },
    descriptionModel: {
      get: function () {
        this.description = this.barter.about.description;
        return this.barter.about.description;
      },
      set: function (description) {
        this.description = description;
      },
    },
    modeModel: {
      get: function () {
        this.mode = this.barter.mode;
        return this.barter.mode;
      },
      set: function (mode) {
        this.mode = mode;
      },
    },
  },
  methods: {
    updateBarter() {
      if (
        this.title &&
        this.description &&
        this.skill &&
        this.interest &&
        this.country &&
        this.city &&
        this.mode
      ) {
        this.loading = true;
        let formData = {
          barter: this.barter.id,
          title: this.title,
          description: this.description,
          country: this.country,
          city: this.city,
          skill: this.skill,
          interest: this.interest,
          mode: this.mode,
        };
        fetch(this.baseUrl + this.apiDir, {
          method: "PUT",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        })
          .then((response) => response.json())
          .then((response) => {
            this.$emit("barterUpdated");
          })
          .catch((err) => console.error(err))
          .finally(() => {
            this.loading = false;
          });
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