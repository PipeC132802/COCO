<template>
  <div v-if="username == currentUsernamePath" class="pl-8 pr-8 pt-6">
    <UserCover :user2Follow="user2Follow" />

    <v-container fluid class="pa-0 mt-0">
      <v-row wrap>
        <v-col tyle="background: red;" tile sm="12" md="8">
          <router-view class="mt-2" />
          <div v-if="pathName == 'Profile'">
            <v-tabs v-model="tab" class="mt-1">
              <v-tab> <v-icon left>mdi-comment</v-icon> Mis Trueques </v-tab>
              <v-tab><v-icon left>mdi-star</v-icon>Mis Reseñas</v-tab>
              <v-tab><v-icon left>mdi-heart</v-icon>Mis Reacciones</v-tab>
            </v-tabs>
            <v-tabs-items v-model="tab">
              <v-tab-item>
                <div class="pa-1" v-if="tab == 0">
                  <NewBarter v-on:newBarterPosted="bartersReload" class="mt-5" v-if="username == user.username" />
                  <BarterList :field="'profile'" />
                </div>
              </v-tab-item>
              <v-tab-item> Reseñas </v-tab-item>
              <v-tab-item> Reacciones </v-tab-item>
            </v-tabs-items>
          </div>
        </v-col>
        <v-col cols="4" tile>
          <UserAbout  />
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
import { mapState } from "vuex";
export default {
  components: {
    UserCover,
    NewBarter,
    UserAbout,
    UserContact,
    User2FollowSuggestion,
    BarterList
  },
  data: () => ({
    username: "",
    tab: null,
    currentUsernamePath: "",
    user2Follow: null,
    pathName: '',
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
    bartersReload(){
      console.log("Nuevo trueque")
    }
    
  },
};
</script>

<style>

</style>