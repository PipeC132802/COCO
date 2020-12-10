<template>
  <div>
    <v-autocomplete
      v-model="areas"
      :items="items"
      chips
      :label="subject == 'skills' ? 'Habilidades' : 'Quiero aprender'"
      item-text="area"
      item-value="area"
      multiple
      required
      :rules="[rules.required]"
      :loading="isLoading"
      :search-input.sync="search"
      hide-no-data
      hide-selected
    >
      <template v-slot:selection="data">
        <v-chip
          v-bind="data.attrs"
          :input-value="data.selected"
          close
          @click="data.select"
          @click:close="remove(data.item)"
          :color="subject == 'skills' ? 'primary darken-1' : 'accent accent-1'"
        >
          {{ data.item.area }}
        </v-chip>
      </template>
      <template v-slot:item="data">
        <template v-if="typeof data.item !== 'object'">
          <v-list-item-content v-text="data.item"></v-list-item-content>
        </template>
        <template v-else>
          <v-list-item-content>
            <v-list-item-title v-html="data.item.area"></v-list-item-title>
          </v-list-item-content>
        </template>
      </template>
    </v-autocomplete>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Areas",
  props: ["subject"],
  data() {
    return {
      autoUpdate: true,
      areas: [],
      isLoading: false,
      entries: [],
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
  beforeUpdate(){
    this.$emit(this.subject, this.areas);
  },
  watch: {
    search(val) {
      // Items have already been loaded
      if (this.items.length > 0) return;

      // Items have already been requested
      if (this.isLoading) return;

      this.isLoading = true;

      fetch(this.baseUrl + this.apiDir + `?area=`, {
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

  methods: {
    remove(item) {
      const index = this.areas.indexOf(item.area);
      if (index >= 0) this.areas.splice(index, 1);
    },
  },
};
</script>

<style>
</style>