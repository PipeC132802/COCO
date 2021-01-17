<template>
  <v-card class="pa-2">
    <v-card-title>
      <v-btn
        icon
        color="primary"
        class="mr-3"
        exact
        :to="{ name: 'Profile', props: { username: $route.params.username } }"
        ><v-icon>mdi-arrow-left-thick</v-icon></v-btn
      >
      Siguiendo
    </v-card-title>
    <v-divider></v-divider>

    <v-card-text class="pb-0" v-if="!following.length">
      <p v-if="$route.params.username == user.username">Aún no sigues a nadie 🤔</p>
      <p v-else>@{{$route.params.username}} aún no sigue a nadie 🤔</p>
    </v-card-text>
    <v-card-text v-else>
      <v-list-item
        class="user-suggest"
        v-for="(followed, i) in following"
        :key="i"
        two-line
      >
        <v-list-item-avatar color="secondary">
          <v-img
            v-if="followed.profile_picture"
            :src="followed.profile_picture"
          ></v-img>
          <span class="white--text" v-else>{{
            followed.name.slice(0, 1)
          }}</span>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title
            :title="followed.name"
            class="link"
            @click="toProfile(followed.username)"
            >{{ followed.name }}</v-list-item-title
          >
          <v-list-item-subtitle :title="'@' + followed.username"
            >@{{ followed.username }}</v-list-item-subtitle
          >
        </v-list-item-content>
        <v-list-item-action
          v-if="user.username && followed.username != user.username"
        >
          <FollowButton :followThisUser="false" :from="user.username" :to="followed.username" 
              :target="$route.params.username == user.username?'self':'other'" :text="true"/>
        </v-list-item-action>
      </v-list-item>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
import FollowButton from "@/components/FollowButton.vue";
export default {
  components:{
    FollowButton,
  },
  data: () => ({
    following: "",
    apiDir: "follow-list/",
    username: "",
  }),
  created() {
    this.username = this.$route.params.username;
    this.getFollowers();
  },
  computed: {
    ...mapState(["baseUrl", "user"]),
  },
  methods: {
    getFollowers() {
      fetch(
        this.baseUrl +
          this.apiDir +
          `?username_target=${this.username}&username_request=${this.user.username}&field=following`
      )
        .then((response) => response.json())
        .then((response) => (this.following = response))
        .catch((err) => console.log(err));
    },
    toProfile(username) {
      this.$router.push({ name: "Profile", params: { username: username } });
    },
  },
};
</script>

<style>
p{
  font-size: 16pt;
}
</style>