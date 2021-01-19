<template>
  <div>
    <v-list-item>
      <v-badge
        overlap
        color="accent white--text"
        bottom
        content="💬"
        offset-x="35"
        offset-y="30"
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
              path: `/${notification.receiver}/barters/${notification.barter.slug}/${notification.barter.id}#comment_${notification.comment.id}`,
            }"
          >
            {{ notification.comment.text }}</router-link
          >
        </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
  </div>
</template>

<script>
export default {
  name: "ReactionNotification",
  props: ["notification"],
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
};
</script>

<style>
</style>