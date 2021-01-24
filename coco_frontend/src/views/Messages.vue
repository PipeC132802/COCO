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
        <v-row v-for="message in messages" :key="message.id">
          <div class="incoming-msg">
            {{ message.text }}
          </div>
          <div class="outgoing-msg ml-auto">
            {{ message.text }}
          </div>
        </v-row>
      </v-card-text>
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
    colors:{
      incoming: '#f06b24fb',
      outgoing: '#3079bdfa',
      bg: '#3636362a'
    }
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
        if(outgoing != null && incoming != null & bg != null){
          
          messagesDiv.style.setProperty("--outgoing-msg-bg", outgoing);
          messagesDiv.style.setProperty("--incoming-msg-bg", incoming);
          messagesDiv.style.setProperty("--background-color", bg);
          this.colors ={
            incoming: incoming,
            outgoing: outgoing,
            bg: bg
          };
        }
      } catch (error) {}
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
  --incoming-msg-bg: #f06b24fb;
  --outgoing-msg-bg: #3079bdfa;
  --background-color: #3636362a;
}

.link-msgs {
  font-size: 14pt;
  font-weight: bold;
  text-decoration: none;
}
.link-msgs:hover{
  text-decoration: underline;
}
.messages {
  max-height: 75vh;
  height: 70vh;
  padding: 10px 30px;
  overflow: auto;
  background: var(--background-color);
  border-radius: 15px;
}
.incoming-msg {
  display: inline-block;
  position: relative;
  margin: 7px 0;
  padding: 10px;
  border-radius: 0px 8px 8px 8px;
  padding-right: 40px;
  max-width: 80%;
  width: auto;
  background: var(--incoming-msg-bg);
  color: #272727;
}
.incoming-msg::before {
  display: block;
  position: absolute;
  top: -10px;
  left: -9.5px;
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
  padding: 10px;
  border-radius: 8px 0px 8px 8px;
  padding-right: 40px;
  max-width: 80%;
  width: auto;
  color: white;
  background: var(--outgoing-msg-bg);
}
.outgoing-msg::before {
  display: block;
  position: absolute;
  top: -10px;
  right: -9.5px;
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
</style>