<template>
  <v-container fluid>
    <v-row justify="center" class="px-0">
      <v-col class="ma-0" cols="12" sm="12" md="4">
        <InboxComponent />
      </v-col>
      <v-col tile class="chatlist" sm="12" md="8">
        <router-view v-if="!change" />
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
  }),
  created() {
    document.title = "Inbox | COCO";
  },
  computed: {
    ...mapState(["user"]),
  },
  watch: {
    $route(to, from) {
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
    },
  },
  methods: {
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
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