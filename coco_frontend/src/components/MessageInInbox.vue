<template>
  <div>
    <v-list two-line>
      <v-list-item
        class="chat"
        active-class="grey lighten-3"
        
        :to="{name:'Messages',params:{id: chat.conversation}}"
        exact
        @mousemove="menu = true"
        @mouseleave="menu = false"
      >
        <v-list-item-avatar color="secondary">
          <v-img
            v-if="chat.opponent.profile_picture"
            :src="chat.opponent.profile_picture"
          ></v-img>
          <span class="white--text" v-else>{{
            chat.opponent.name.slice(0, 1).toUpperCase()
          }}</span>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>
            <router-link
              class="title--text link"
              :title="chat.opponent.name"
              :to="{
                name: 'Profile',
                params: { username: chat.opponent.username },
              }"
              >{{ chat.opponent.name }}</router-link
            ><span class="grey--text ml-2" :title="'@' + chat.opponent.username"
              >@{{ chat.opponent.username }}</span
            >
          </v-list-item-title>
          <v-list-item-subtitle>
            <div v-if="typing">
              <span class="primary--text">Escribiendo ...</span>
            </div>
            <div v-else>
              <span v-if="chat.sender == user.username">

                <v-icon title="Enviado" class="mr-1" v-if="!chat.read" small>mdi-check</v-icon>
                <v-icon title="Visto" class="mr-1" v-else color="primary" small>mdi-check-all</v-icon>
              </span>
              <span  :title="chat.text">
                {{ chat.text }}
              </span>
            </div>
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <span>
            <small
              :class="chat.unread_messages ? 'info--text' : ''"
              :title="getHour | capitalize"
              >{{ getHour | capitalize }}</small
            >
          </span>
          <span>
            <v-avatar
              v-if="chat.unread_messages"
              size="25"
              color="info darken-1"
            >
              <small class="white--text">{{ getUnreadMsgs }}</small>
            </v-avatar>
            <v-btn v-if="menu" class="ml-1" x-small icon>
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
import { mapState } from "vuex";
export default {
  name: "MessageInInbox",
  props: ["chat"],
  data: () => ({
    menu: false,
    typing: false,
    seen: true,
    websocket: null,
  }),
  computed: {
    ...mapState(["wsBase", "user"]),
    getHour() {
      let getHour = moment(this.chat.send).locale("es").format("hh:mm a");
      return getHour;
    },
    getUnreadMsgs() {
      if (this.chat.unread_messages > 10) {
        return "+10";
      } else {
        return this.chat.unread_messages;
      }
    },
  },
  methods: {
    chooseChat() {
      this.$router.push({ name: "Messages", params: { id: this.chat.conversation } });
    },
    connect() {
      let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";
      this.websocket = new WebSocket(
        protocol + this.wsBase + "/ws/chat/" + this.chat.conversation + "/"
      );
      this.websocket.onopen = () => {
        console.info(
          "conectado exitosamente inbox!",
          this.conversation.conversation
        );
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));
          const socketData = JSON.parse(data);
          if (
            socketData.type === "type_message" &&
            socketData.sender != this.user.username
          ) {
            this.typing = socketData.typing;
          } else if (socketData.type === "chat_message") {
            this.chat.text = socketData.text;
            this.chat.send = socketData.send;
            this.chat.sender = socketData.sender;
          } else if (
            socketData.type == "seen_message" &&
            socketData.receiver == this.user.username
          ) {
            this.conversation.unread_messages = socketData.unread_messages;
          }
        };
      };
      this.websocket.onclose = () => {};
    },
  },
};
</script>

<style>

</style>