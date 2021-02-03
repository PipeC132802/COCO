<template>
  <div v-if="authentication.userIsAuthenticated">
    <v-btn
      @click="followUser"
      :outlined="!followed"
      color="success"
      :title="followed ? 'Siguiendo' : 'Seguir'"
    >
      <v-icon> mdi-account-plus </v-icon>
      <span class="ml-2" v-if="text">{{ verbose }}</span>
    </v-btn>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { sendNotificationViaWS } from "../functions.js";

export default {
  props: ["from", "to", "target", "text"],
  data: () => ({
    followed: 0,
    apiDir: "follow-user/",
    verbose: "",
  }),
  computed: {
    ...mapState(["authentication", "baseUrl", "wsBase", "user"]),
  },
  created() {
    this.followed = this.followThisUser;
    this.getFollowStatus();
  },
  methods: {
    ...mapMutations(["updateProfileFollowStatus"]),
    getFollowStatus() {
      fetch(
        this.baseUrl +
          this.apiDir +
          `?username_from=${this.from}&username_to=${this.to}`,
        {
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
          },
        }
      )
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.followed = response.follow_this_user;
          if (this.text) {
            this.getVerbose();
          }
        });
    },
    followUser() {
      if (this.from) {
        let formData = {
          username_to: this.to,
          username_from: this.from,
          target: this.target,
        };
        fetch(this.baseUrl + this.apiDir, {
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
            this.followed = response.follow_this_user;
            this.getVerbose();
            if (this.from == this.$route.params.username) {
              let followObj = {
                followers: response.followers,
                following: response.following,
                followThisUser: response.follow_this_user,
              };
              this.updateProfileFollowStatus(followObj);
            }
            this.$emit("followObj", response);
            this.notifyUser(response.notification);

          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
    getVerbose() {
      this.verbose = this.followed ? "Siguiendo" : "Seguir";
    },
    notifyUser(response) {
      if (response) {
        let sockedData = {
          type: "new_notification",
          sender: response.user_from.username,
          receiver: response.user_to,
          userFrom: response.user_from,
          action: response.action,
          created: response.created,
          field: response.field,

        };
        sendNotificationViaWS(sockedData, this.wsBase, response.user_to);
      }
    },
  },
};
</script>

<style>
</style>