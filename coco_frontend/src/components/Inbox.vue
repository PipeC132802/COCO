<template>
  <div>
    <v-card flat>
      <v-card-text class="card-text">
        <div v-if="loading">
          <v-skeleton-loader
            v-for="index in 7"
            :key="index"
            type="list-item-avatar-two-line"
          ></v-skeleton-loader>
        </div>

        <MessageInInbox
          v-for="chat in chats"
          :key="chat.id"
          :chat="chat"
        />
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
import MessageInInbox from "../components/MessageInInbox.vue";
export default {
  name: "Inbox",
  components: {
    MessageInInbox,
  },
  data: () => ({
    apiDir: "inbox/",
    chats: [],
    loading: true,
  }),
  computed: {
    ...mapState(["user", "authentication", "baseUrl"]),
  },
  mounted() {
    this.getChatList();
  },
  methods: {
    getChatList() {
      fetch(this.baseUrl + this.apiDir, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((response) => (this.chats = response))
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
  max-height: 83vh;
  height: 83vh;
  overflow: auto;
}
.chat{
  border-radius: 5px;
}
.chat:hover {
  background-color: rgb(219, 219, 219);
  cursor: pointer;
  border-radius: 5px;
}
</style>