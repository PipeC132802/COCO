<template>
  <div>
    <div v-if="loading">
      <v-skeleton-loader
        v-for="index in 10"
        :key="index"
        type="list-item-avatar-two-line"
      ></v-skeleton-loader>
    </div>
    <p class="pl-5"></p>
    <v-alert
      v-if="!notifications[0]"
      color="warning"
      dark
      icon="mdi-bell-remove"
      dense
    >
      Aún no tienes notificaciones
    </v-alert>
    <v-card
      class="ma-2 px-0 mx-0"
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
import { mapState, mapMutations } from "vuex";
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
    ...mapState(["baseUrl", "authentication", "notification"]),
  },
  mounted() {
    this.retrieveNotifications();
  },
  methods: {
    ...mapMutations(["notificationStatus"]),
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
          this.notificationStatus({
            unread_notifications: 0,
            unread_messages: this.notification.unread_messages,
          });
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