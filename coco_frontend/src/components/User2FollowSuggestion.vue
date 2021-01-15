<template>
  <v-card elevation="3" v-if="users.length">
    <v-card-title> Sugerencias </v-card-title>
    <v-divider></v-divider>
    <v-card-text class="mt-0 pa-0">
      <v-list-item class="user-suggest" v-for="(userSuggestion, i) in users" :key="i" two-line>
        <v-list-item-avatar color="secondary"> 
          <v-img
            v-if="userSuggestion.profile_picture"
            :src="userSuggestion.profile_picture"
          ></v-img>
          <span class="white--text" v-else>{{ userSuggestion.name.slice(0, 1) }}</span>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title :title=" userSuggestion.name" class="link" @click="toProfile(userSuggestion.username)">{{
            userSuggestion.name
          }}</v-list-item-title>
          <v-list-item-subtitle :title="'@'+userSuggestion.username">@{{ userSuggestion.username }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
              <FollowButton :text="false" :from="user.username" :to="userSuggestion.username" 
              :target="$route.params.username == user.username?'self':'other'"  />
        </v-list-item-action>
      </v-list-item>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import FollowButton from "@/components/FollowButton.vue";
export default {
  name: "User2FollowSuggestion.vue",
  components:{
    FollowButton
  },
  data: () => ({
    apiDir: "suggest-users/",
    users: "",
    followThisUser: false,
  }),
  computed: {
    ...mapState(["baseUrl", "user", "authentication"]),
  },
  created() {
    this.users2Follow();
  },
  beforeUpdate() {},
  methods: {
    ...mapMutations(["updateProfileFollowStatus"]),

    users2Follow() {
      fetch(this.baseUrl + this.apiDir + `?user_except=${this.$route    .params.username}`, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
          "Content-Type": "application/json",
        },
      })
        .then((respose) => {
          return respose.json();
        })
        .then((respose) => (this.users = respose));
    },
    toProfile(username) {
      this.$router.push({ name: "Profile", params: { username: username } });
    },
  },
};
</script>

<style>

.link:hover {
  text-decoration: underline;
  cursor: pointer;
}
.user-suggest:hover{
    background: #09243d0a;
}
</style>