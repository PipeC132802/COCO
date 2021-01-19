<template>
  <v-card outlined class="ma-2 pa-0 notification" elevation="3">
    <v-card-text class="pa-0">
      <v-list class="ma-0" three-line>
        <ReactionNotification
          v-if="notification.field == 'reaction'"
          :notification="notification"
        />
        <CommentNotification
          v-if="notification.field == 'comment'"
          :notification="notification"
        />
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapMutations } from "vuex";
import ReactionNotification from "../components/subcomponents/ReactionNotification.vue";
import CommentNotification from "../components/subcomponents/CommentNotification.vue";
export default {
  name: "NotificationBox",
  props: ["notification"],
  components: {
    ReactionNotification,
    CommentNotification
  },
  data: () => ({
    timeOut: 5, // segs
  }),
  computed: {},
  methods: {
    ...mapMutations(["removeNotification"]),
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
  },
  created() {
    this.sleep(this.timeOut * 1000).then(() => {
      this.removeNotification();
    });
  },
};
</script>

<style>
.notification {
  transition: all ease-in 2000ms;
}
</style>