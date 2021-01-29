<template>
  <v-container class="pt-3" fluid>
    <v-row justify="center" class="px-0">
      <v-col
        class="pa-0"
        id="inbox-chats"
        cols="12"
        sm="12"
        md="4"
        v-if="inboxView"
      >
        <InboxComponent />
      </v-col>
      <v-col tile class="chatlist" cols="12 pt-0 ma-0" sm="12" md="8">
        <router-view v-on:main="changeInboxViewStatus" v-if="!change" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import InboxComponent from "../components/Inbox.vue";
import { mapState } from "vuex";
import { decript } from "../functions.js";
export default {
  components: {
    InboxComponent,
  },
  data: () => ({
    chat: null,
    change: false,
    inboxView: true,
  }),
  created() {
    document.title = "Inbox | COCO";
   
  },
  computed: {
    ...mapState(["user", "breakpoints"]),
  },
  watch: {
    $route(to, from) {
      let screenWidth = window.screen.width;
      if (this.breakpoints.xs > screenWidth) {
        if (to.name != "Inbox") {
          this.change = true;
          this.sleep(5).then(() => {
            this.change = false;
            this.inboxView = false;
          });
        } else {
          this.inboxView = true;
        }
      } else {
        try {
          if (
            decript(this.user.username, to.params.id) !=
            decript(this.user.username, from.params.id)
          ) {
            this.change = true;
            this.sleep(5).then(() => {
              this.change = false;
            });
          }
        } catch (error) {}
      }
    },
  },
  methods: {
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    changeInboxViewStatus(status) {
      this.inboxView = status;
    },
  },
};
</script>

<style>
.chatlist {
  border-left: 1px solid rgb(211, 211, 211);
  margin: 0%;
}
</style>