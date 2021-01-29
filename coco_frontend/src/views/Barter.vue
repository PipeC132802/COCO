<template>
  <v-container fluid>
    <v-row>
      <v-col md="3" lg="3" class="px-3 big-devices">
        <AccountBox />
      </v-col>
      <v-col tile cols="12" sm="12" md="6" lg="6">
        <BarterList :field="'detail'" :pk="$route.params.pk" />
      </v-col>
      <v-col md="3" lg="3">
        <User2FollowSuggestions class="mx-2" />
        <CompanyInfo  class="big-devices mx-1" />
      </v-col>
              <CompanyInfo  class="small-devices mx-1" />
    </v-row>
    <v-footer>

    </v-footer>
  </v-container>
</template>

<script>
import User2FollowSuggestions from "../components/User2FollowSuggestion.vue";
import AccountBox from "../components/AccountBox.vue";
import BarterList from "../components/BarterList.vue";
import CompanyInfo from "../components/CompanyInfo.vue";
export default {
  components: {
    User2FollowSuggestions,
    AccountBox,
    BarterList,
    CompanyInfo,
  },
  beforeCreate() {
    document.title = "Trueque | COCO";
  },
};
</script>

<style>
</style>