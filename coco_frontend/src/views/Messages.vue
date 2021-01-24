<template>
  <div>
    <v-card flat>
      <v-list two-line>
        <v-list-item>
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

      <v-card-text id="msgs-list" class="messages">
        <v-row v-for="message in messages" :key="message.id" :class="typing?'mb-5':''">
          <div
            v-if="message.sender_username != user.username"
            class="incoming-msg"
          >
            {{ message.text }}
            <small
              :title="formatDate(message.created) | capitalize"
              class="msg-footer"
            >
              {{ getHour(message.created) }}
            </small>
          </div>
          <div v-else class="outgoing-msg ml-auto">
            {{ message.text }}
            <small class="msg-footer">
              <span :title="formatDate(message.created) | capitalize">
                {{ getHour(message.created) }}
              </span>
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
      <v-card-actions>
        <v-container fluid>
          <v-row>
            <v-btn class="mt-1 mr-1" icon>
              <v-icon>mdi-emoticon-outline</v-icon>
            </v-btn>
            <v-text-field
              rounded
              outlined
              dense
              v-model="msg"
              label="Escribe tu mensaje"
              solo
              :append-outer-icon="msg ? 'mdi-send' : ''"
            ></v-text-field>
          </v-row>
        </v-container>
      </v-card-actions>
    </v-card>
    <v-bottom-sheet v-model="sheet">
      <v-sheet class="text-center" height="220px">
        <ColorPicker
          v-if="sheet"
          :incoming="colors.incoming"
          :outgoing="colors.outgoing"
          :bg="colors.bg"
          v-on:outgoingColor="outgoingColorSet"
          v-on:incomingColor="incomingColorSet"
          v-on:bgColor="bgColorSet"
        />
      </v-sheet>
    </v-bottom-sheet>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { decript } from "../functions.js";
import ColorPicker from "../components/subcomponents/ColorPicker.vue";
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
    msg: "",
    typing: false,
  }),
  mounted() {
    this.getMessages();
    this.setColors2Divs();
  },
  computed: {
    ...mapState(["user", "authentication", "baseUrl", "wsBase", "chat"]),
  },
  methods: {
    decriptId() {
      return decript(this.user.username, this.$route.params.id);
    },
    getMessages() {
      fetch(this.baseUrl + this.apiDir + `?conversation=${this.decriptId()}`, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          this.messages = response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    setColors2Divs() {
      var messagesDiv = document.getElementById("msgs-list");
      try {
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
      } catch (error) {}
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
  },
};
</script>

<style>
:root {
  --incoming-msg-bg: #09243df5;
  --outgoing-msg-bg: #3079bdfa;
  --background-color: #3636362a;
}

.link-msgs {
  font-size: 14pt;
  font-weight: bold;
  text-decoration: none;
}
.link-msgs:hover {
  text-decoration: underline;
}
.messages {
  position: relative;
  max-height: 65vh;
  height: 70vh;
  padding: 10px 30px;
  overflow: auto;
  background: var(--background-color);
  border-radius: 15px 15px 0 0;
}
.incoming-msg {
  display: inline-block;
  position: relative;
  margin: 7px 0;
  padding: 10px 70px 10px 10px;
  border-radius: 0px 8px 8px 8px;
  max-width: 80%;
  width: auto;
  background: var(--incoming-msg-bg);
  color: white;
}
.incoming-msg::before {
  display: block;
  position: absolute;
  top: -10px;
  left: -9px;
  content: "";
  width: 0;
  height: 0;
  border-right: 10px solid transparent;
  border-top: 10px solid transparent;
  border-left: 10px solid transparent;
  border-bottom: 10px solid var(--incoming-msg-bg);
  transform: rotate(45deg);
  border-radius: 5px;
}
.outgoing-msg {
  display: inline-block;
  position: relative;
  margin: 7px 0;
  padding: 10px 70px 15px 10px;
  border-radius: 8px 0px 8px 8px;
  max-width: 80%;
  width: auto;
  color: white;
  background: var(--outgoing-msg-bg);
}
.outgoing-msg::before {
  display: block;
  position: absolute;
  top: -10px;
  right: -9px;
  content: "";
  width: 0;
  height: 0;

  border-right: 10px solid transparent;
  border-top: 10px solid transparent;
  border-left: 10px solid var(--outgoing-msg-bg);
  border-bottom: 10px solid transparent;
  transform: rotate(-135deg);
  border-radius: 5px;
}
.msg-footer {
  position: absolute;
  right: 8px;
  bottom: 0px;
  color: white;
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
.typing-container{
  position: absolute;
  bottom: 30px;
}
</style>