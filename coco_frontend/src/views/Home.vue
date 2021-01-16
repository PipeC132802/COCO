<template>
  <div>
    <v-container fluid>
      <v-row wrap>
        <v-col class="px-4" tile sm="12" md="8" lg="9" xl="10">
          <NewBarter />
          <BarterList class="mt-5" :field="'newsfeed'" />
        </v-col>
        <v-col sm="12" md="4" lg="3" xl="2" class="pt-0 mt-0">
          <User2FollowSuggestion class="mt-2" />
          <CompanyInfo class="mx-1" />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
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
  },
};
</script>
