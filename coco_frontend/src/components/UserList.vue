<template>
  <v-container fluid class="pa-0" >
    <v-card class="pa-0 mb-4" elevation="3" v-for="(userInList, i) in users"
          :key="i"
          two-line>
      <v-card-text class="mt-0 pa-0">
        <v-list-item
          class="user-suggest"
          
        >
          <v-list-item-avatar color="secondary">
            <v-img
              v-if="userInList.profile_picture"
              :src="userInList.profile_picture"
            ></v-img>
            <span class="white--text" v-else>{{
              userInList.name.slice(0, 1)
            }}</span>
          </v-list-item-avatar>
          <v-list-item-content>
            <v-list-item-title
              :title="userInList.name"
              >
              <router-link class="link title--text" :to="{
                  name: 'Profile',
                  params: { username: userInList.user },
                }">{{ userInList.name }}</router-link>
              </v-list-item-title
            >
            <v-list-item-subtitle :title="'@' + userInList.user"
              >@{{ userInList.user }}</v-list-item-subtitle
            >
          </v-list-item-content>
          <v-list-item-action v-if="user.username != userInList.user">
            <FollowButton


              :text="false"
              :from="user.username"
              :to="userInList.user"
              target="other"
            />
          </v-list-item-action>
        </v-list-item>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import FollowButton from "../components/FollowButton.vue"
import {mapState} from "vuex";
export default {
  name: "UserList",
  props: ["users"],
  components:{
      FollowButton
  },
  computed:{
      ...mapState(['user'])
  }
};
</script>

<style>
</style>