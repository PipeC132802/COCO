<template>
  <v-container fluid>
    <v-card outlined elevation="5" class="ma-0 pa-0">
      <v-row justify="center" class="pa-0">
        <v-avatar class="mx-auto mt-4" size="70">
          <img
            alt="user"
            v-if="account.profile_picture"
            :src="account.profile_picture"
          />
          <span v-else>{{ account.name.slice(0, 1) }}</span>
        </v-avatar>
      </v-row>
      <v-row justify="center">
        <router-link
          class="name title--text link"
          :title="account.name"
          :to="{ name: 'Profile', params: { username: account.user } }"
        >
          <v-card-title class="pb-0 mt-0 pt-0">
            {{ account.name }}

            <v-card-subtitle :title="account.user" class="ml-1 px-0">
              (@{{ account.user }})
            </v-card-subtitle>
          </v-card-title>
        </router-link>
      </v-row>

      <v-card-text class="mt-0 pt-0">
        <blockquote v-if="account.bio" class="blockquote">
          <p class="mb-0 mt-5 ml-0">
            {{ account.bio }}
          </p>
        </blockquote>
      </v-card-text>
      <v-card-actions class="pt-0" v-if="username !== user.username">
        <v-row justify="center">
          <FollowButton
            class="mb-2"
            :from="user.username"
            :to="username"
            :target="$route.params.username == user.username ? 'self' : 'other'"
            :text="true"
          />
        </v-row>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import FollowButton from "../components/FollowButton.vue";
export default {
  name: "AccountBox",
  components: {
    FollowButton,
  },
  data: () => ({
    username: "",
    account: "",
    apiDir: "user-about/",
  }),
  computed: {
    ...mapState(["baseUrl", "user"]),
  },
  beforeMount() {
    this.username = this.$route.params.username;
    this.getAccountAbout();
  },
  methods: {
    getAccountAbout() {
      fetch(this.baseUrl + this.apiDir + `?username=${this.username}`)
        .then((response) => response.json())
        .then((response) => {
          this.account = response;
        })
        .catch((err) => console.error(err));
    },
  },
};
</script>

<style>
.blockquote {
  font-size: 1.15rem;
  border-left: 0.3rem solid#478CCC;
  color: #6c757d;
  font-family: "Open Sans", "Segoe UI", "Roboto";
  line-height: 1.2;
  margin: 0 auto;
  max-width: 100%;
  position: relative;
  width: 100%;
}
.blockquote:before {
  font-size: 6.875rem;
  color: #478ccc;
  content: "\201C";
  font-family: "Noto Serif", "Georgia", "Karla", serif;
  font-size: 5.5rem;
  height: 3.75rem;
  left: 0.2rem;
  line-height: 1;
  max-width: 3.75rem;
  position: absolute;
  text-align: inherit;
  top: 0.1rem;
  width: 100%;
}
.blockquote:after {
  content: "";
}
.name {
  font-size: 16pt;
}
</style>