<template>
  <div>
    <v-container fluid>
      <v-row wrap>
        <v-col  class="px-7" sm="12" md="8" lg="9" xl="10"> 
        <p class="display-1 ml-1" v-if="!$route.query.q">Te puede interesar</p>
        <BarterList class="ma-0" v-if="!$route.query.q" :field="'recommendations'" />  
        <SearchResults v-else />
        </v-col>
        <v-col sm="12" md="4" lg="3" xl="2">
          <User2FollowSuggestion />
          <CompanyInfo />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import User2FollowSuggestion from "../components/User2FollowSuggestion.vue";
import BarterList from "../components/BarterList.vue";
import CompanyInfo from "../components/CompanyInfo.vue";
import SearchResults from "../components/SearchResults.vue";

export default {
  components: {
    User2FollowSuggestion,
    BarterList,
    CompanyInfo,
    SearchResults
  },
  created() {
    document.title = "Explorar | COCO";
  },
};
</script>

<style>
.suggestions{
  font-size: 12pt;
}
</style>