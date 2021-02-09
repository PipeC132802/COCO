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
      <v-col
        tile
        class="chatlist mt-5 pa-0 px-3"
        cols="12"
        sm="12"
        md="8"
      >
        <router-view v-on:main="changeInboxViewStatus" v-if="!change" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import InboxComponent from "../components/Inbox.vue";
import { mapState } from "vuex";
import { decript, addMetaTagData } from "../functions.js";
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
    let metaObj = [
        {property: 'og:title', content: "'Truequea' tus conocimientos con COCO"},
        {property: 'og:description', content: "Busca personas con conocimientos en lo que quieres aprender e interés en lo que sabes. ¡Truequea tus habilidades!"},
        {property: 'description', content: "Busca personas con conocimientos en lo que quieres aprender e interés en lo que sabes. ¡Truequea tus habilidades!"},
        {property: 'title', content: "'Truequea' tus conocimientos con COCO"},
        {property: 'og:type', content: "website"},
      ];
      addMetaTagData(metaObj);
  },
  computed: {
    ...mapState(["user", "breakpoints"]),
  },
  watch: {
    $route(to, from) {
      let screenWidth = window.screen.width;
      if (this.breakpoints.sm > screenWidth) {
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