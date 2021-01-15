<template>
  <v-container class="pa-0">
    <p class="display-1 title--text text-center ma-0">
      Resultados para
      <span :title="$route.query.q" class="primary--text">
        {{ $route.query.q }}
      </span>
    </p>
    <p class="text-center ma-0">
      {{ results.barters.length + results.users.length }}
      {{
        "resultado" + pluralize(results.barters.length + results.users.length)
      }}
      en {{ results.time }} segundos
    </p>
    <v-tabs v-model="tab">
      <v-tab
        ><v-icon left>mdi-clipboard-list</v-icon
        ><span class="tab-title">Todos</span>
      </v-tab>
      <v-tab
        ><v-icon left>mdi-text-box-multiple</v-icon
        ><span class="tab-title">Trueques</span></v-tab
      >
      <v-tab
        ><v-icon left>mdi-account-group</v-icon
        ><span class="tab-title">Usuarios</span></v-tab
      >
    </v-tabs>
    <v-tabs-items v-model="tab">
      <v-tab-item>
        <div class="pa-1">
          <div v-if="results.barters" class="mt-2 ml-3">
            {{
              results.barters.length +
              " trueque" +
              pluralize(results.barters.length)
            }}
          </div>
          <div v-for="barter in results.barters" :key="barter.id">
            <BarterList :field="'detail'" :pk="barter.id" />
          </div>
          <v-divider class="mb-2"></v-divider>
          <div v-if="results.users" class="mt-2 ml-3">
            {{
              results.users.length +
              " usuario" +
              pluralize(results.users.length)
            }}
          </div>
          <UserList :users="results.users" />
        </div>
      </v-tab-item>
      <v-tab-item>
        <div>
          <div v-if="results.barters" class="mt-2 ml-3">
            {{
              results.barters.length +
              " trueque" +
              pluralize(results.barters.length)
            }}
          </div>
          <div v-for="barter in results.barters" :key="barter.id">
            <BarterList :field="'detail'" :pk="barter.id" />
          </div>
        </div>
      </v-tab-item>
      <v-tab-item>
        <div class="ma-0">
          <div v-if="results.users" class="mt-2 ml-3">
            {{
              results.users.length +
              " usuario" +
              pluralize(results.users.length)
            }}
          </div>
          <UserList :users="results.users" />
        </div>
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import BarterList from "../components/BarterList.vue";
import UserList from "../components/UserList.vue";
export default {
  name: "SearchResults",
  components: {
    BarterList,
    UserList,
  },
  data: () => ({
    tab: null,
    results: {
      users: [],
      barters: [],
      time: "",
    },
    apiDir: "search/",
  }),
  computed: {
    ...mapState(["baseUrl"]),
  },
  watch: {
    $route(to, from) {
      this.getSearchResults();
    },
  },
  beforeMount() {
    document.title = "Búsqueda | COCO";
    this.getSearchResults();
  },
  methods: {
    getSearchResults() {
      fetch(this.baseUrl + this.apiDir + "?q=" + this.$route.query.q)
        .then((response) => response.json())
        .then((response) => (this.results = response))
        .catch((err) => console.error(err));
    },
    pluralize: function (val) {
      if (val > 1 || val == 0) {
        return "s";
      } else {
        return "";
      }
    },
  },
};
</script>

<style>
.tab-title {
  text-transform: capitalize;
}
</style>