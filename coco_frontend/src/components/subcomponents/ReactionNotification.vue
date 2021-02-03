<template>
  <div>
    <v-list-item>
      <v-badge
        offset-x="35"
        :offset-y="place ? '25' : '30'"
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
        <v-list-item-title>
          <router-link
            class="link title--text"
            :to="{
              name: 'Profile',
              params: { username: notification.userFrom.username },
            }"
          >
            {{ notification.userFrom.name }}
          </router-link>
          <span class="grey--text">@{{ notification.userFrom.username }}</span>
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
        <v-row
          justify="start"
          class="grey--text pl-3"
          :title="timeSince | capitalize"
        >
          <v-icon left small>mdi-progress-clock</v-icon>
          <small>{{ timeSince | capitalize }}</small>
        </v-row>
      </v-list-item-content>
    </v-list-item>
  </div>
</template>

<script>
import moment from "moment";

export default {
  name: "ReactionNotification",
  props: ["notification", "place"],
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
    timeSince: function () {
      let timeSince = moment(this.notification.created).locale("es").fromNow();
      return timeSince;
    },
  },
};
</script>

<style>
</style>