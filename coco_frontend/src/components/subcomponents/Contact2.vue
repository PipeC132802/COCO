<template>
  <div>
    <v-row align="center">
      <v-col cols="12" md="6">
        <v-autocomplete
          v-model="country"
          :items="items"
          :loading="isLoading"
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
              <v-list-item-content v-text="data.item"></v-list-item-content>
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
      <v-col cols="12" md="6">
        <v-text-field
          class="pa-0"
          v-model="city"
          label="Ciudad"
          :rules="[rules.required]"
          required
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="4" md="2">
        <v-text-field
          class="mb-1 pa-0"
          v-model="prefix"
          label="Prefijo"
          :rules="[rules.valid]"
        ></v-text-field>
      </v-col>
      <v-col cols="8" sm="10">
        <v-text-field
          class="mb-1 pa-0"
          v-model="cellphone"
          label="Número de teléfono"
          :rules="[rules.cellValid]"
        ></v-text-field>
      </v-col>
    </v-row>
  </div>
</template>

<script>
// Archivo de datos 'postres.json'
import countries from "@/json/countriescodes.json";
export default {
  name: "Contact",
  data() {
    return {
      descriptionLimit: 60,
      entries: [],
      isLoading: false,
      search: null,
      country: "",
      city: "",
      prefix: "",
      cellphone: "",
      rules: {
        required: (value) => !!value || "Obligatorio",
        valid: (value) =>
          !/^(\+)?[0-9]{2,4}$/.test(value) ? "Prefijo inválido" : true,
        cellValid: (value) =>
          !/^[0-9]{1,14}$/.test(value) ? "Número inválido" : true,
      },
    };
  },
  computed: {
    items() {
      return countries.map((country) => {
        return country;
      });
    },
  },
  watch: {
    country() {
      this.prefix = "+" + this.country.phone_code;
    },
  },
  beforeUpdate() {
    let contactObj = {
      country: this.country.nombre,
      city: this.city,
      phone: this.prefix + " " + this.cellphone,
    };
    this.$emit("contact", contactObj);
  },

  methods: {},
};

//
</script>

<style>
</style>