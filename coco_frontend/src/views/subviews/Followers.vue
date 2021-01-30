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
      Seguidores
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text class="pb-0" v-if="!followers.length">
      <p v-if="$route.params.usernme == user.username">Nadie te sigue 😞</p>
      <p v-else>@{{ $route.params.username }} aún no tiene seguidores 😞</p>
    </v-card-text>
    <v-card-text v-else>
      <v-lazy
        v-for="(follower, i) in followers"
        :key="i"
        transition="fade-transition"
      >
        <v-list-item class="user-suggest" two-line>
          <v-list-item-avatar color="secondary">
            <v-img
              v-if="follower.profile_picture"
              :src="follower.profile_picture"
            ></v-img>
            <span class="white--text" v-else>{{ follower.name.slice(0, 1) }}</span>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              :title="follower.name"
              class="link"
              @click="toProfile(follower.username)"
              >{{ follower.name }}</v-list-item-title
            >
            <v-list-item-subtitle :title="'@' + follower.username"
              >@{{ follower.username }}</v-list-item-subtitle
            >
          </v-list-item-content>
          <v-list-item-action
            v-if="user.username && follower.username != user.username"
          >
            <FollowButton
              :followThisUser="false"
              :from="user.username"
              :to="follower.username"
              :target="
                $route.params.username == user.username ? 'self' : 'other'
              "
              :text="true"
            />
          </v-list-item-action>
        </v-list-item>
      </v-lazy>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
import FollowButton from "@/components/FollowButton.vue";
export default {
  components: {
    FollowButton,
  },
  data: () => ({
    followers: "",
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
          `?username_target=${this.username}&username_request=${this.user.username}&field=followers`
      )
        .then((response) => response.json())
        .then((response) => (this.followers = response))
        .catch((err) => console.error(err));
    },
    toProfile(username) {
      this.$router.push({ name: "Profile", params: { username: username } });
    },
  },
};
</script>

<style>
p {
  font-size: 16pt;
}
</style>