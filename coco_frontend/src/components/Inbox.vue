<template>
  <div>
    <v-card flat>
      <v-card-text class="card-text pa-0">
        <div v-if="loading">
          <v-skeleton-loader
            v-for="index in 7"
            :key="index"
            type="list-item-avatar-two-line"
          ></v-skeleton-loader>
        </div>
        <div v-else>
          <v-alert
          v-if="!chats.length"
            color="primary darken-3"
            dark
            icon="mdi-message-bulleted-off"
            dense
            class="mx-2 mt-3"
          >
            No tienes chats
          </v-alert>
          <MessageInInbox
            v-for="(chat, index) in chats"
            :key="chat.id"
            :chatObj="chat"
            :index="index"
            v-on:reloadChats="getChatList()"
          />
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import MessageInInbox from "../components/MessageInInbox.vue";
export default {
  name: "Inbox",
  components: {
    MessageInInbox,
  },
  data: () => ({
    apiDir: "inbox/",
    loading: true,
  }),
  computed: {
    ...mapState(["user", "authentication", "baseUrl", "chats"]),
  },
  mounted() {
    this.getChatList();
  },
  methods: {
    ...mapMutations(["setChats"]),
    getChatList() {
      fetch(this.baseUrl + this.apiDir, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          this.setChats(response);
        })
        .catch((err) => console.error(err))
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>

<style>
.card-text {
  display: block;
  max-height: 85vh;
  height: 85vh;
  overflow: auto;
}
.chat {
  border-radius: 5px;
}
.chat:hover {
  background-color: rgb(219, 219, 219);
  cursor: pointer;
  border-radius: 5px;
}
</style>