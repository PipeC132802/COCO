<template>
  <div>
    <v-container fluid>
      <v-row wrap>
        <v-col class="pt-0" tile cols="12" sm="12" md="8" lg="9" xl="10">
          <NewBarter class="new-barter mb-5" />
          <BarterList :field="'newsfeed'" />
        </v-col>
        <v-col sm="12" md="4" lg="3" xl="2" class="pt-0 mt-0">
          <User2FollowSuggestion class="mt-2" />
          <CompanyInfo class="mx-1 big-devices" />
        </v-col>
      </v-row>
    </v-container>
    <v-footer>
      <CompanyInfo class="small-device" />
    </v-footer>
  </div>
</template>

<script>
// @ is an alias to /src
import {addMetaTagData} from "../functions.js";
import NewBarter from "@/components/NewBarter";
import BarterList from "@/components/BarterList.vue";
import User2FollowSuggestion from "@/components/User2FollowSuggestion.vue";
import CompanyInfo from "@/components/CompanyInfo.vue";

export default {
  name: "Home",

  components: {
    NewBarter,
    BarterList,
    User2FollowSuggestion,
    CompanyInfo,
  },
  created() {
    document.title = "Inicio | COCO";
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
@media (max-width: 920px) {
  .new-barter {
    display: none;
  }
}
</style>