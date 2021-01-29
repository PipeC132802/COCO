<template>
  <div class="pa-0" v-if="username == currentUsernamePath">
    <UserCover :user2Follow="user2Follow" />

    <v-container fluid class="pa-0 mt-0">
      <v-row class="pa-0 ma-0" wrap>
        <v-col tile class="pa-0" cols="12" sm="12" md="8">
          <router-view class="mt-2" />
          
        </v-col>
        <v-col cols="12" md="4" tile>
          <UserAbout />
          <UserContact />
          <User2FollowSuggestion
            v-if="$route.params.username != user.username"
            v-on:followUser="followUser"
            class="ma-2 mt-3"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import UserCover from "@/components/UserCover.vue";
import NewBarter from "@/components/NewBarter.vue";
import User2FollowSuggestion from "@/components/User2FollowSuggestion.vue";
import UserAbout from "@/components/subcomponents/UserAbout.vue";
import UserContact from "@/components/subcomponents/UserContact.vue";
import BarterList from "@/components/BarterList.vue";
import ReviewsList from "../components/ReviewsList.vue";
import { mapState } from "vuex";
export default {
  components: {
    UserCover,
    NewBarter,
    UserAbout,
    UserContact,
    User2FollowSuggestion,
    BarterList,
    ReviewsList,
  },
  data: () => ({
    username: "",
    tab: null,
    currentUsernamePath: "",
    user2Follow: null,
    pathName: "",
  }),
  watch: {
    $route(to, from) {
      this.currentUsernamePath = to.params.username;
      this.pathName = this.$route.name;
    },
  },
  beforeUpdate() {
    this.sleep(5).then(() => {
      this.username = this.$route.params.username;
    });
  },
  created() {
    this.username = this.$route.params.username;
    this.pathName = this.$route.name;
    this.currentUsernamePath = this.$route.params.username;
  },

  computed: {
    ...mapState(["user"]),
  },
  methods: {
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    followUser(followUserObj) {
      this.user2Follow = followUserObj;
    },
  },
};
</script>

<style>
</style>