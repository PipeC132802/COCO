<template>
  <div>
    <v-row>
      <v-col>
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
      <v-col>
        <v-text-field
          class="mb-1"
          v-model="city"
          label="Ciudad"
          :rules="[rules.required]"
          required
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col sm="2">
        <v-text-field
          class="mb-1"
          v-model="countryCode"
          label="Prefijo"
          :rules="[rules.valid]"
        ></v-text-field>
      </v-col>
      <v-col sm="10">
        <v-text-field
          class="mb-1"
          v-model="phone"
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
      country: null,
      city: "",
      search: null,
      countryCode: null,
      phone: "",
      rules: {
        required: (value) => !!value || "Obligatorio",
        valid: (value) =>
          !/^(\+)?[0-9]{2,4}$/.test(value) ? "Prefijo inválido" : true,
        cellValid: (value) =>
          !/^[0-9]{1,14}$/.test(value) ? "Número inválido" : true,
      },
    };
  },
  beforeUpdate() {
    if (this.country !== null) {
      this.countryCode = "+" + this.country.phone_code;
      let contactObj = {
        country: this.country.nombre,
        city: this.city,
        phone: this.countryCode + this.phone,
      };
     
      this.$emit("contact", contactObj);
    }
  },
  computed: {
    items() {
      return countries.map((country) => {
        return country;
      });
    },
  },

  watch: {},

  methods: {},
};

//
</script>

<style>
</style>