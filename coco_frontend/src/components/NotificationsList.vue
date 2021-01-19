<template>
  <div>
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
    </v-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import ReactionNotification from "../components/subcomponents/ReactionNotification.vue";
export default {
  name: "NotificationsList",
  components: {
    ReactionNotification,
  },
  data: () => ({
    notifications: [],
    apiDir: "notifications/",
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
          this.$emit("unreadNotifications", 0);
          console.log(response);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style>
</style>