<template>
  <v-container fluid>
    <v-row wrap>
      <v-col class="pa-0 " tile sm="12" md="8" lg="8" xl="9">
        <NotificationsList />
      </v-col>
      <v-col cols="12" sm="12" md="4" lg="4" xl="3" class="pt-0 mt-0">
        <User2FollowSuggestion class="mt-2" />
        <CompanyInfo class="mx-1 big-devices" />
      </v-col>
    </v-row>
    <v-footer>
      <CompanyInfo class="mx-1 small-device" />
    </v-footer>
  </v-container>
</template>

<script>
import User2FollowSuggestion from "../components/User2FollowSuggestion.vue";
import CompanyInfo from "../components/CompanyInfo.vue";
import NotificationsList from "../components/NotificationsList.vue";
export default {
  name: "Notifications",
  components: {
    User2FollowSuggestion,
    CompanyInfo,
    NotificationsList,
  },
  created() {
    document.title = "Notificaciones | COCO";
  },
};
</script>

<style>
</style>