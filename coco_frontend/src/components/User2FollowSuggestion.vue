<template>
  <v-card>
    <v-card-title> Te puede interesar </v-card-title>
    <v-card-text>
      <v-list-item two-line>
          <v-list-item-avatar>
            <v-img :src="item.avatar"></v-img>
          </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>Two-line item</v-list-item-title>
          <v-list-item-subtitle>Secondary text</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn
          @click="followUser"
          :outlined="!userP.followThisUser"
          color="success"
          :title="userP.followThisUser ? 'Seguido' : 'Seguir'"
          class="mr-3"
        >
          <v-icon left> mdi-account-plus </v-icon>
          <span>{{userP.followThisUser ? 'Siguiendo' : 'Seguir'}}</span>
        </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "User2FollowSuggestion.vue",
};
</script>

<style>
</style>