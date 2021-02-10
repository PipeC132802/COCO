<template>
  <div>
    <v-container fluid>
      <v-row wrap>
        <v-col cols="12 mt-0 pb-0 px-4" sm="12" md="8" lg="9" xl="10">
          <p class="title-interest ml-1" v-if="!$route.query.q">
            Te puede interesar
          </p>
          <BarterList
            class="ma-0"
            v-if="!$route.query.q"
            :field="'recommendations'"
          />
          <SearchResults v-else />
        </v-col>
        <v-col cols="12 pt-0" sm="12" md="4" lg="3" xl="2">
          <User2FollowSuggestion />
          <CompanyInfo class="big-devices" />
        </v-col>
      </v-row>
    </v-container>
  
  </div>
</template>

<script>
import {addMetaTagData} from "../functions.js";
import User2FollowSuggestion from "../components/User2FollowSuggestion.vue";
import BarterList from "../components/BarterList.vue";
import CompanyInfo from "../components/CompanyInfo.vue";
import SearchResults from "../components/SearchResults.vue";


export default {
  components: {
    User2FollowSuggestion,
    BarterList,
    CompanyInfo,
    SearchResults,
  },
  created() {
    document.title = "Explorar | COCO";
    let metaObj = [
        {property: 'og:title', content: "'Truequea' tus conocimientos con COCO"},
        {property: 'og:description', content: "Busca personas con conocimientos en lo que quieres aprender e interés en lo que sabes. ¡Truequea tus habilidades!"},
        {property: 'description', content: "Busca personas con conocimientos en lo que quieres aprender e interés en lo que sabes. ¡Truequea tus habilidades!"},
        {property: 'title', content: "'Truequea' tus conocimientos con COCO"},
      ];
      addMetaTagData(metaObj);
  },
};
</script>

<style>
.suggestions {
  font-size: 12pt;
}
.title-interest {
  font-size: calc(1em + 1vw);
}
</style>