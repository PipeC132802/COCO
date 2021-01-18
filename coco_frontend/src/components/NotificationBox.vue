<template>
  <v-card class="ma-2 notification" elevation="3">
    {{ notification }}
    {{index}}
  </v-card>
</template>

<script>
import { mapMutations } from "vuex";
export default {
  name: "NotificationBox",
  props: ["notification", "index"],
  data: () => ({
    timeOut: 5, // segs
  }),
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
.notification{
    transition: all ease-in 2000ms;
}
</style>