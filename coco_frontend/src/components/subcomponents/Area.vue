<template>
  <div>
    <v-autocomplete
      v-model="area"
      :items="items"
      :label="subject == 'skill' ? 'Habilidad en' : 'Interés en'"
      item-text="area"
      item-value="area"
      required
      :rules="[rules.required]"
      :loading="isLoading"
      :search-input.sync="search"
      hide-no-data
      hide-selected
    >
    </v-autocomplete>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Area",
  props: ["subject"],
  data() {
    return {
      autoUpdate: true,
      isLoading: false,
      entries: [],
      area: "",
      rules: {
        required: (value) => !!value || "Obligatorio",
      },
      apiDir: "area-list/",
      search: null,
    };
  },
  computed: {
    ...mapState(["authentication", "baseUrl"]),
    items() {
      return this.entries.map((entry) => {
        return entry;
      });
    },
  },
  beforeUpdate() {
    this.$emit(this.subject, this.area);
  },
  watch: {
    search(val) {
      // Items have already been loaded

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      fetch(this.baseUrl + this.apiDir + `?area=${val.trim()}`, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}  `,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          this.entries = response;
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => (this.isLoading = false));
    },
  },
};
</script>

<style>
</style>