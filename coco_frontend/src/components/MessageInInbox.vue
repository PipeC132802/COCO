<template>
  <div>
    <v-list class="pt-0 pb-0 chat-element" two-line>
      <v-list-item
        :class="
          chatElement.conversation ==
          msgDecrypted(user.username, $route.params.id)
            ? 'chatElement active-chatElement'
            : 'chatElement'
        "
        exact
        :to="{
          name: 'Messages',
          params: { id: encryptId(chatElement.conversation) },
        }"
        @mousemove="menu = true"
        @mouseleave="menu = false"
        @click="chatSelected"
      >
        <v-list-item-avatar color="secondary">
          <v-img
            v-if="chatElement.opponent.profile_picture"
            :src="chatElement.opponent.profile_picture"
          ></v-img>
          <span class="white--text" v-else>{{
            chatElement.opponent.name.slice(0, 1).toUpperCase()
          }}</span>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>
           {{ chatElement.opponent.name }}<span
              class="grey--text ml-2"
              :title="'@' + chatElement.opponent.username"
              >@{{ chatElement.opponent.username }}</span
            >
          </v-list-item-title>
          <v-list-item-subtitle>
            <div v-if="typing">
              <span class="primary--text">Escribiendo ...</span>
            </div>
            <div v-else>
              <span v-if="chatElement.sender == user.username">
                <v-icon
                  title="Enviado"
                  class="mr-1"
                  v-if="!chatElement.read"
                  small
                  >mdi-check</v-icon
                >
                <v-icon title="Visto" class="mr-1" v-else color="primary" small
                  >mdi-check-all</v-icon
                >
              </span>
              <span :title="chatElement.text">
                {{
                  msgDecrypted(chatElement.sender_username, chatElement.text)
                }}
              </span>
            </div>
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <span>
            <small
              :class="chatElement.unread_messages ? 'info--text' : ''"
              :title="getHour | capitalize"
              >{{ getHour | capitalize }}</small
            >
          </span>
          <span>
            <v-avatar
              v-if="chatElement.unread_messages"
              size="25"
              color="info darken-1"
            >
              <small class="white--text">{{ getUnreadMsgs }}</small>
            </v-avatar>
            <v-btn v-if="menu" color="primary" class="ml-1" x-small icon>
              <v-icon>mdi-menu-down</v-icon>
            </v-btn>
          </span>
        </v-list-item-action>
      </v-list-item>
      <v-divider inset></v-divider>
    </v-list>
  </div>
</template>

<script>
import moment from "moment";
import { mapMutations, mapState, mapActions } from "vuex";
import { encrypt, decript } from "../functions.js";
export default {
  name: "MessageInInbox",
  props: ["chatObj"],
  data: () => ({
    menu: false,
    typing: false,
    seen: true,
    websocket: null,
    sound: require("../assets/sounds/notifications/newmessage.ogg"),
  }),
  computed: {
    ...mapState(["wsBase", "user", "secretKey", "chats", "chat", "notification"]),
    chatElement: {
      get: function () {
        return this.chatObj;
      },
      set: function (val) {},
    },
    getUnreadMsgs() {
      if (this.chatElement.unread_messages > 10) {
        return "+10";
      } else {
        return this.chatElement.unread_messages;
      }
    },
    getHour() {
      let getHour = moment(this.chatElement.created)
        .locale("es")
        .format("hh:mm a");
      return getHour;
    },
  },
  mounted() {
    this.connect();
  },
  beforeDestroy() {
    this.websocket.close();
    this.websocket = null;
  },
  methods: {
    ...mapMutations(["setChat", "msgReceivedInbox", 'notificationStatus']),
    getChatIndex() {
      let chatElement = this.chats.find(
        (chatElement) =>
          chatElement.conversation == this.chatElement.conversation
      );
      return this.chats.indexOf(chatElement);
    },
    msgDecrypted(dataKey, msgEncrypted) {
      var decryptedMsg = "";
      try {
        decryptedMsg = decript(dataKey, msgEncrypted);
      } catch (error) {
        decryptedMsg = 0;
      }
      return decryptedMsg;
    },
    encryptId(id) {
      return encrypt(id, this.user.username);
    },
    chatSelected() {
      this.setChat(this.chatElement);
    },
    play() {
      let notificationDiv = document.getElementById("notification");
      notificationDiv.innerHTML = `<audio src="${this.sound}" autoplay></audio>`;
    },
    connect() {
      let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";
      this.websocket = new WebSocket(
        protocol +
          this.wsBase +
          "/ws/chat/" +
          this.chatElement.conversation +
          "/"
      );
      this.websocket.onopen = () => {
  
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));
          const socketData = JSON.parse(data);
          if (
            socketData.type === "type_message" &&
            socketData.sender != this.user.username
          ) {
            this.typing = socketData.typing;
          } else if (socketData.type === "chat_message") {
            this.chatElement.text = socketData.text;
            this.chatElement.sender_username = socketData.sender_username;
            this.chatElement.created = socketData.created;
            if (socketData.sender_username != this.user.username) {
              this.chatElement.unread_messages = socketData.unread_messages;
              this.notificationStatus({unread_messages: socketData.unread_messages, unread_notifications: this.notification.unread_notifications});
              this.play();
            } else this.chatElement.unread_messages = 0;
            this.setChat(this.chatElement);

            this.typing = false;
          } else if (socketData.type == "seen_message") {
            this.chatElement.unread_messages = socketData.unread_messages;
          }
          if (socketData.type == "chat_message") {
            this.msgReceivedInbox(this.getChatIndex());
          }
        };
      };
      this.websocket.onclose = () => {};
    },
  },
};
</script>

<style>
.link {
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}
.active-chatElement {
  border-radius: 5px;
  background: rgb(206, 206, 206);
}
.chat-element:hover {
  background: rgb(231, 231, 231);
}
</style>