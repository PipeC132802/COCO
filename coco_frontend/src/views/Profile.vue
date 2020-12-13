<template>
  <div class="pl-8 pr-8 pt-6">
    <UserCover />

    <v-container fluid class="pa-0 mt-0">
      <v-row>
        <v-col tyle="background: red;" tile sm="12" md="8">
          <v-tabs v-model="tab" class="mt-1">
            <v-tab> <v-icon left>mdi-comment</v-icon> Publicaciones </v-tab>
            <v-tab><v-icon left>mdi-star</v-icon> Reseñas</v-tab>
            <v-tab><v-icon left>mdi-heart</v-icon> Me gusta</v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item>
              <NewBarter v-if="username == user.username" />
            </v-tab-item>
            <v-tab-item>
                Rese;a
            </v-tab-item>
            <v-tab-item>
                Me gusta
            </v-tab-item>
          </v-tabs-items>
        </v-col>
        <v-col tile>
          <UserAbout />
          <UserContact />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import UserCover from "@/components/UserCover.vue";
import NewBarter from "@/components/NewBarter.vue";
import UserAbout from "@/components/subcomponents/UserAbout.vue";
import UserContact from "@/components/subcomponents/UserContact.vue";
import { mapState } from "vuex";
export default {
  components: {
    UserCover,
    NewBarter,
    UserAbout,
    UserContact,
  },
  data: () => ({
    username: "",
    tab: null,
    items: ["web", "shopping", "videos", "images", "news"],
    text:
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
  }),
  created() {
    this.username = this.$route.params.username;
  },
  computed: {
    ...mapState(["user"]),
  },
};
</script>

<style>
</style>