<template>
  <div class="pl-8 pr-8 pt-6">
    <UserCover />
    <v-container fluid class="pa-0 mt-4">
      <v-row>
        <v-col tyle="background: red;" tile sm="12" md="8">
          <NewBarter v-if="username==user.username" />
        </v-col>
        <v-col tile>
         <div style="background: orange; height: 500px; width: 100%;"></div>
        </v-col>

      </v-row>
    </v-container>
  </div>
</template>

<script>
import UserCover from "@/components/UserCover.vue";
import NewBarter from "@/components/NewBarter.vue";
import UserAbout from "@/components/subcomponents/UserAbout.vue";
import { mapState } from "vuex";
export default {
  components: {
    UserCover,
    NewBarter,
  },
  data: () => ({
    username: ''
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