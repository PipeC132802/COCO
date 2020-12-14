<template>
  <v-card class="pa-2">
    <v-card-title>
      <v-btn
        icon
        color="primary"
        class="mr-3"
        exact
        :to="{ name: 'Profile', props: { username: $route.params.username } }"
        ><v-icon>mdi-arrow-left-thick</v-icon></v-btn
      >
      Seguidores
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      <v-list-item
        class="user-suggest"
        v-for="(user, i) in users"
        :key="i"
        two-line
      >
        <v-list-item-avatar>
          <v-img
            v-if="user.profile_picture"
            :src="user.profile_picture"
          ></v-img>
          <span v-else>{{ user.name.slice(0, 1) }}</span>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title
            :title="user.name"
            class="link"
            @click="toProfile(user.username)"
            >{{ user.name }}</v-list-item-title
          >
          <v-list-item-subtitle :title="'@' + user.username"
            >@{{ user.username }}</v-list-item-subtitle
          >
        </v-list-item-content>
        <v-list-item-action>
          <v-btn
            @click="followUser(user)"
            :outlined="!followThisUser"
            color="success"
            :title="followThisUser ? 'Seguido' : 'Seguir'"
            class="mr-3"
          >
            <v-icon left> mdi-account-plus </v-icon>
            <span>{{ followThisUser ? "Siguiendo" : "Seguir" }}</span>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-card-text>
  </v-card>
</template>

<script>
export default {};
</script>

<style>
</style>