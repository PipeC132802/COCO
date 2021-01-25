<template>
  <div>
    <div v-if="loading">
      <v-skeleton-loader
        v-for="index in 10"
        :key="index"
        type="list-item-avatar-two-line"
      ></v-skeleton-loader>
    </div>
    <p class="pl-5 display-1" v-if="!notifications[0].length">
      Nada por aquí 
    </p>
    <v-card
      class="ma-2"
      v-for="notification in notifications"
      :key="notification.id"
    >
      <reaction-notification
        :place="true"
        :notification="notification"
        v-if="notification.field == 'reaction'"
      />
      <comment-notification
        :place="true"
        :notification="notification"
        v-else-if="notification.field == 'comment'"
      />
      <follow-user-notification
        :place="true"
        :notification="notification"
        v-else-if="notification.field == 'follow'"
      />
    </v-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import ReactionNotification from "../components/subcomponents/ReactionNotification.vue";
import CommentNotification from "../components/subcomponents/CommentNotification.vue";
import FollowUserNotification from "../components/subcomponents/FollowUserNotification.vue";
export default {
  name: "NotificationsList",
  components: {
    ReactionNotification,
    CommentNotification,
    FollowUserNotification,
  },
  data: () => ({
    notifications: [],
    apiDir: "notifications/",
    loading: true,
  }),
  computed: {
    ...mapState(["baseUrl", "authentication"]),
  },
  mounted() {
    this.retrieveNotifications();
  },
  methods: {
    // TO-DO Find why this overload the server
    retrieveNotifications() {
      fetch(this.baseUrl + this.apiDir, {
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          
          this.notifications = response;
          this.$root.$emit("notificationsReaded");
        })
        .catch((err) => {
          console.error(err);
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style>
</style>