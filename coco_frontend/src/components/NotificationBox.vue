<template>
  <v-card class="ma-2 notification" elevation="3">
    <v-card-text>
      <v-list three-line>
        <v-list-item>
          <v-badge
            offset-x="35"
            offset-y="30"
            overlap
            color="accent"
            bottom
            :content="getEmoji"
          >
            <v-list-item-avatar color="secondary">
              <v-img
                v-if="notification.userFrom.profile_picture"
                :src="notification.userFrom.profile_picture"
              ></v-img>
              <span class="white--text" v-else>{{
                notification.userFrom.name.slice(0, 1)
              }}</span>
            </v-list-item-avatar>
          </v-badge>
          <v-list-item-content>
            <v-list-item-title
              >{{ notification.userFrom.name }}
              <span class="grey--text"
                >@{{ notification.userFrom.username }}</span
              >
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ notification.action }}:
              <router-link
                class="link title--text"
                :to="{
                  name: 'Barter',
                  params: {
                    username: notification.receiver,
                    slug: notification.barter.slug,
                    pk: notification.barter.id,
                  },
                }"
              >
                {{ notification.barter.title }}</router-link
              >
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
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
  computed: {
    getEmoji: function () {
      let msg = "";
      switch (this.notification.reaction) {
        case 1:
          msg = "😎";
          break;
        case 2:
          msg = "🤩";
          break;
        case 3:
          msg = "🤔";
          break;

        default:
          break;
      }
      return msg;
    },
  },
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