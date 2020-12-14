<template>
  <v-card v-if="users.length">
    <v-card-title> Puedes seguir </v-card-title>
    <v-divider></v-divider>
    <v-card-text class="mt-0 pa-0">
      <v-list-item class="user-suggest" v-for="(user, i) in users" :key="i" two-line>
        <v-list-item-avatar>
          <v-img
            v-if="user.profile_picture"
            :src="user.profile_picture"
          ></v-img>
          <span v-else>{{ user.name.slice(0, 1) }}</span>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title :title=" user.name" class="link" @click="toProfile(user.username)">{{
            user.name
          }}</v-list-item-title>
          <v-list-item-subtitle :title="'@'+user.username">@{{ user.username }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn
            @click="followUser(user)"
            :outlined="!followThisUser"
            color="success"
            :title="followThisUser ? 'Seguido' : 'Seguir'"
            class="mr-3"
          >
            <v-icon left> mdi-account-plus </v-icon>
            <span>{{ followThisUser ? "Siguiendo" : "Seguir" }}</span>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState, mapMutations } from "vuex";
export default {
  name: "User2FollowSuggestion.vue",
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
    followUser(user) {
      if (this.user.username) {
        let formData = {
          username_to: user.username,
          username_from: this.user.username,
        };
        fetch(this.baseUrl + "follow-user/", {
          method: "POST",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        })
          .then((response) => {
            return response.json();
          })
          .then((response) => {
            this.followThisUser = response.follow_this_user;
            if (this.user.username == this.$route.params.username) {
                this.updateProfileFollowStatus(response)
            }
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
  },
};
</script>

<style>
.link {
}
.link:hover {
  text-decoration: underline;
  cursor: pointer;
}
.user-suggest:hover{
    background: #09243d0a;
}
</style>