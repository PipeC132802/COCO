<template>
  <div>
    <v-card id="chat" class="chat-body" flat>
      <v-row class="px-1" align="center">
        <v-btn small color="primary" class="ml-2" :to="{ name: 'Inbox' }" icon>
          <v-icon>mdi-arrow-left</v-icon>
        </v-btn>
        <v-col class="pt-0 pb-0">
          <v-list class="pt-0 pb-0" dense two-line>
            <v-list-item dense class="px-0">
              <v-list-item-avatar color="secondary">
                <v-img
                  v-if="chat.opponent.profile_picture"
                  :src="chat.opponent.profile_picture"
                ></v-img>
                <span class="white--text" v-else>{{
                  chat.opponent.name.slice(0, 1).toUpperCase()
                }}</span>
              </v-list-item-avatar>
              <v-list-item-content class="pt-0 pb-0">
                <v-list-item-title>
                  <router-link
                    class="title--text link-msgs"
                    :title="chat.opponent.name"
                    :to="{
                      name: 'Profile',
                      params: { username: chat.opponent.username },
                    }"
                    >{{ chat.opponent.name }}</router-link
                  >
                </v-list-item-title>
                <v-list-item-subtitle>
                  <span class="grey--text" :title="'@' + chat.opponent.username"
                    >@{{ chat.opponent.username }}</span
                  >
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn @click="sheet = !sheet" icon>
                  <v-icon>mdi-palette</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
            <v-divider></v-divider>
          </v-list>
        </v-col>
      </v-row>
      <v-card-text id="msgs-list" class="messages ma-0">
        <v-row
          v-for="message in messages"
          :key="message.id"
          :class="typing ? 'mb-2' : ''"
        >
          <div
            v-if="message.sender_username != user.username"
            class="incoming-msg"
          >
            {{ decriptText(message.sender_username, message.text) }}
            <small
              :title="formatDate(message.created) | capitalize"
              class="msg-footer mr-1"
            >
              {{ getHour(message.created) }}
            </small>
          </div>
          <div v-else class="outgoing-msg ml-auto">
            {{ decriptText(user.username, message.text) }}
            <small class="msg-footer">
              {{ getHour(message.created) }}
              <span>
                <v-icon class="ml-1" v-if="!message.read" small
                  >mdi-check</v-icon
                >
                <v-icon class="ml-1" v-else small color="white"
                  >mdi-check-all</v-icon
                >
              </span>
            </small>
          </div>
        </v-row>
        <div class="typing-container" v-if="typing">
          <div class="typing-animation">
            <v-avatar class="typing-avatar" size="30" color="secondary">
              <v-img
                v-if="chat.opponent.profile_picture"
                :src="chat.opponent.profile_picture"
              ></v-img>
              <span class="white--text" v-else>{{
                chat.opponent.name.slice(0, 1).toUpperCase()
              }}</span>
            </v-avatar>
            <span style="left: 25px; top: -7px" class="typing-avatar"
              >Escribiendo...</span
            >
          </div>
        </div>
      </v-card-text>
      <v-container class="px-3 pt-3 pb-0" fluid>
        <v-row>
          <v-btn class="mt-1 mr-1" icon>
            <v-icon>mdi-emoticon-outline</v-icon>
          </v-btn>
          <v-text-field
            @keyup="typingMessage"
            @keyup.enter="sendMessage"
            @focus="seenMsg"
            rounded
            outlined
            dense
            v-model="msg"
            label="Escribe tu mensaje"
            solo
            @click:append-outer="sendMessage"
            :append-outer-icon="msg ? 'mdi-send' : ''"
          ></v-text-field>
        </v-row>
      </v-container>
    </v-card>
    <ColorPicker
      v-if="sheet"
      v-on:sheetStatus="updateSheetStatus"
      :incoming="colors.incoming"
      :outgoing="colors.outgoing"
      :bg="colors.bg"
      v-on:outgoingColor="outgoingColorSet"
      v-on:incomingColor="incomingColorSet"
      v-on:bgColor="bgColorSet"
    />
  </div>
</template>

<script>
import { mapState, mapMutations } from "vuex";
import { decript, encrypt } from "@/functions.js";
import ColorPicker from "@/components/subcomponents/ColorPicker.vue";
import moment from "moment";

export default {
  name: "Messages",
  components: {
    ColorPicker,
  },
  data: () => ({
    messages: [],
    message: "",
    apiDir: "messages/",
    sheet: false,
    colors: {
      incoming: "#09243df5",
      outgoing: "#3079bdfa",
      bg: "#3636362a",
    },
    room: null,
    msg: "",
    typing: false,
    change: false,
  }),
  mounted() {
    this.getMessages();
    this.setColors2Divs();
    let screenWidth = window.screen.width;
    if (this.breakpoints.xs > screenWidth) {
      this.$emit("main", false);
    } else {
      this.$emit("main", true);
    }
     
  },
  beforeDestroy() {
    this.websocket.close();
    this.websocket = null;
  },
  computed: {
    ...mapState([
      "user",
      "authentication",
      "baseUrl",
      "wsBase",
      "chat",
      "notification",
      "breakpoints",
    ]),
  },
  methods: {
    ...mapMutations(["notificationStatus"]),
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    decriptText(dataKey, dataEncrypted) {
      var text = decript(dataKey, dataEncrypted);
      if (this.room == null) this.room = text;
      return text;
    },
    getMessages() {
      fetch(
        this.baseUrl +
          this.apiDir +
          `?conversation=${this.decriptText(
            this.user.username,
            this.$route.params.id.toString()
          )}`,
        {
          method: "GET",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
          },
        }
      )
        .then((response) => response.json())
        .then((response) => {
          this.messages = response;
          this.connect();
        })
        .catch((err) => {
          console.error(err);
        });
    },
    sendMessage() {
      if (this.msg.length) {
        this.websocket.send(
          JSON.stringify({
            type: "chat_message",
            conversation: this.room,
            sender: this.user.username,
            receiver: this.chat.opponent.username,
            text: encrypt(this.msg, this.user.username),
            read: false,
          })
        );
        this.msg = "";
      }
    },
    typingMessage() {
      let sender = this.user.username;
      if (this.msg.length) {
        this.websocket.send(
          JSON.stringify({
            type: "type_message",
            sender: sender,
            receiver: this.chat.opponent.username,
            typing: true,
          })
        );
      } else {
        this.websocket.send(
          JSON.stringify({
            type: "type_message",
            sender: sender,
            receiver: this.chat.opponent.username,
            typing: false,
          })
        );
      }
    },
    seenMsg() {
      if (this.chat.sender_username != this.user.username) {
        let sender = this.user.username;
        this.websocket.send(
          JSON.stringify({
            type: "seen_message",
            sender: sender,
            receiver: this.chat.sender_username,
            seen: true,
            room: this.room,
          })
        );
      }

      /* if (
        this.messages.length &&
        this.messages[0].sender !== this.user.username &&
        !this.messages[0].read
      ) {
        let sender = this.user.username;
        this.websocket.onopen = () =>
          this.websocket.send(
            JSON.stringify({
              type: "seen_message",
              sender: sender,
              receiver: this.chat.username,
              seen: true,
              room: this.room,
            })
          );
      } */
    },
    connect() {
      let protocol = document.location.protocol == "http:" ? "ws://" : "wss://";
      this.websocket = new WebSocket(
        protocol + this.wsBase + "/ws/chat/" + this.room + "/"
      );
      this.websocket.onopen = () => {
        console.info("conectado exitosamente!", this.room);
        this.websocket.onmessage = ({ data }) => {
          // this.messages.unshift(JSON.parse(data));
          const socketData = JSON.parse(data);
          if (
            socketData.type === "type_message" &&
            socketData.sender != this.user.username
          ) {
            this.typing = socketData.typing;
          } else if (socketData.type === "chat_message") {
            this.messages.unshift(socketData);
            this.typing = false;
            if (socketData.sender_username == this.user.username) {
              this.seenMsg();
            }
          } else if (socketData.type === "seen_message") {
            this.checkSeen();
            this.notificationStatus({
              unread_notifications: this.notification.unread_notifications,
              unread_messages: 0,
            });
          }
        };
      };
      this.websocket.onclose = () => {};
    },
    checkSeen() {
      this.messages.forEach((message) => {
        if (
          message.sender_username == this.user.username &&
          message.read == false
        ) {
          message.read = true;
        }
      });
    },
    updateSheetStatus(status) {
      this.sheet = status;
    },
    setColors2Divs() {
      var messagesDiv = document.getElementById("msgs-list");
      let outgoing = localStorage.getItem("outgoing-msgs");
      let incoming = localStorage.getItem("incoming-msgs");
      let bg = localStorage.getItem("bg-color");
      if (outgoing != null && (incoming != null) & (bg != null)) {
        messagesDiv.style.setProperty("--outgoing-msg-bg", outgoing);
        messagesDiv.style.setProperty("--incoming-msg-bg", incoming);
        messagesDiv.style.setProperty("--background-color", bg);
        this.colors = {
          incoming: incoming,
          outgoing: outgoing,
          bg: bg,
        };
      }
    },
    getHour(dateTime) {
      let getHour = moment(dateTime).locale("es").format("hh:mm a");
      return getHour;
    },
    formatDate(dateTime) {
      return moment(dateTime)
        .locale("es")
        .format("MMMM D [de] YYYY [a las] hh:mm a");
    },
    outgoingColorSet(color) {
      var messagesDiv = document.getElementById("msgs-list");
      messagesDiv.style.setProperty("--outgoing-msg-bg", color);
      localStorage.setItem("outgoing-msgs", color);
      this.colors.outgoing = color;
    },
    incomingColorSet(color) {
      var messagesDiv = document.getElementById("msgs-list");
      messagesDiv.style.setProperty("--incoming-msg-bg", color);
      localStorage.setItem("incoming-msgs", color);
      this.colors.incoming = color;
    },
    bgColorSet(color) {
      var messagesDiv = document.getElementById("msgs-list");
      messagesDiv.style.setProperty("--background-color", color);
      localStorage.setItem("bg-color", color);
      this.colors.bg = color;
    },
    gotoBottom() {
      var elem = document.getElementById("chat");
      var container = document.getElementById("msgs-list");
      container.scrollTop = Math.floor(elem.offsetHeight);
    },
  },
};
</script>

<style>
body {
  background: white;
}
:root {
  --incoming-msg-bg: #09243df5;
  --outgoing-msg-bg: #3079bdfa;
  --background-color: #3636362a;
}
.chat-body {
  height: 85vh;
  background: red;
}
.link-msgs {
  font-size: 14pt;
  font-weight: bold;
  text-decoration: none;
}
.link-msgs:hover {
  text-decoration: underline;
}
.inbox-chats-active {
  display: block;
}
.incoming-msg {
  display: inline-block;
  position: relative;
  margin: 7px 0;
  padding: 10px 10% 2% 10px;
  border-radius: 0px 13px 13px 13px;
  max-width: 80%;
  width: auto;
  background: var(--incoming-msg-bg);
  color: white;
  text-shadow: 0px 0px 1px rgba(0, 0, 0, 1);
}
/*.incoming-msg::before {
  display: block;
  position: absolute;
  top: -10px;
  left: -8px;
  content: "";
  width: 0;
  height: 0;
  border-right: 10px solid transparent;
  border-top: 10px solid transparent;
  border-left: 10px solid transparent;
  border-bottom: 10px solid var(--incoming-msg-bg);
  transform: rotate(45deg);
  border-radius: 5px;
}*/
.outgoing-msg {
  display: inline-block;
  position: relative;
  margin: 7px 0;
  padding: 10px 12% 2% 10px;
  border-radius: 13px 0px 13px 13px;
  max-width: 80%;
  width: auto;
  color: white;
  background: var(--outgoing-msg-bg);
  text-shadow: 0px 0px 1px rgba(0, 0, 0, 1);
}
/*.outgoing-msg::before {
  display: block;
  position: absolute;
  top: -10px;
  right: -8px;
  content: "";
  width: 0;
  height: 0;

  border-right: 10px solid transparent;
  border-top: 10px solid transparent;
  border-left: 10px solid var(--outgoing-msg-bg);
  border-bottom: 10px solid transparent;
  transform: rotate(-135deg);
  border-radius: 5px;
}*/
.messages {
  display: flex;
  flex-direction: column-reverse;
  position: relative;

  margin: 20px 0px;
  height: calc(100vh - 190px);
  width: 100%;
  padding: 10px 6%;
  overflow: auto;
  background: var(--background-color);
  border-radius: 15px 15px 0 0;
  scroll-snap-type: y proximity;
}
@media (max-width: 920px) {
  .inbox-chats {
    display: none;
  }

  .incoming-msg {
    padding: 10px 20% 8% 10px;
  }
  .outgoing-msg {
    min-width: 80px;
    padding: 10px 20% 8% 10px;
  }
}
@media (min-width: 920px) {
  .messages {
    height: calc(100vh - 230px);
  }
}

.msg-footer {
  position: absolute;
  right: 8px;
  bottom: 0px;
  color: white;
  font-size: 7pt;
  text-shadow: 0px 0px 1px rgba(0, 0, 0, 1);
}
.typing-avatar {
  position: absolute;
  top: -13px;
  left: -12px;
}
.typing-animation {
  background: rgba(41, 98, 255, 0.3);
  width: 25px;
  height: 25px;
  position: relative;
  border-radius: 100%;
  border: solid 10px rgba(41, 98, 255, 0.3);
  animation: play 2s ease infinite;
  /*     -webkit-backface-visibility: hidden;
    -moz-backface-visibility: hidden;
    -ms-backface-visibility: hidden;
    backface-visibility: hidden; */
}

@keyframes play {
  0% {
    transform: scale(1);
  }
  15% {
    box-shadow: 0 0 0 5px rgba(41, 98, 255, 0.3);
  }
  25% {
    box-shadow: 0 0 0 10px rgba(41, 98, 255, 0.3),
      0 0 0 20px rgba(41, 98, 255, 0.15);
  }
  25% {
    box-shadow: 0 0 0 15px rgba(41, 98, 255, 0.3),
      0 0 0 30px rgba(41, 98, 255, 0.15);
  }
}
.typing-container {
  position: relative;
  margin: 25px 0%;
}
.v-messages, .v-text-field__details{
  display: none;
}
</style>