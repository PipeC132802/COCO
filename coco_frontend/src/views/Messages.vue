<template>
  <div>
    <v-card>
      asdasd
      <v-card-title class="pt-0 pb-0">
        <v-list two-line>
          <v-list-item>
            <v-list-item-avatar size="45" color="secondary">
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
                >
                  {{ chat.opponent.name }}</router-link
                >
              </v-list-item-title>
              <v-list-item-subtitle>
                <span class="grey--text" :title="'@' + chat.opponent.username"
                  >@{{ chat.opponent.username }}</span
                >
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="messages pt-0">
        <v-list two-line>
          <template v-for="message in messages">
            <v-container :key="message.id" fluid>
              <v-row v-for="i in 10" :key="i">

                <div class="incoming-msg">
                  {{ message.text }}
                </div>
                <div class="outgoing-msg ml-auto">
                  {{ message.text }}
                </div>
              </v-row>
            </v-container>
          </template>
        </v-list>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Messages",
  data: () => ({
    messages: [],
    message: "",
    apiDir: "messages/",
  }),
  mounted() {
    this.getMessages();
  },
  computed: {
    ...mapState(["user", "authentication", "baseUrl", "wsBase"]),
  },
  methods: {
    getMessages() {
      fetch(
        this.baseUrl + this.apiDir + `?conversation=${this.$route.params.id}`,
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
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style scoped>
.link {
  font-size: 14pt;
  font-weight: bold;
}
.messages {
  max-height: 80vh;
  height: 70vh;
  overflow: auto;
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
  color: white;
  background-color: #f06a24;
}
.incoming-msg::before {
  display: block;
  position: absolute;
  top: -10px;
  left: -5px;
  content: "";
  width: 0;
  height: 0;
  border-right: 10px solid transparent;
  border-top: 10px solid transparent;
  border-left: 10px solid transparent;
  border-bottom: 10px solid #f06a24;
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
  background: rgba(0, 84, 153, 1);
  background: -moz-linear-gradient(
    left,
    rgba(0, 84, 153, 1) 0%,
    rgba(48, 121, 189, 1) 100%
  );
  background: -webkit-gradient(
    left top,
    right top,
    color-stop(0%, rgba(0, 84, 153, 1)),
    color-stop(100%, rgba(48, 121, 189, 1))
  );
  background: -webkit-linear-gradient(
    left,
    rgba(0, 84, 153, 1) 0%,
    rgba(48, 121, 189, 1) 100%
  );
  background: -o-linear-gradient(
    left,
    rgba(0, 84, 153, 1) 0%,
    rgba(48, 121, 189, 1) 100%
  );
  background: -ms-linear-gradient(
    left,
    rgba(0, 84, 153, 1) 0%,
    rgba(48, 121, 189, 1) 100%
  );
  background: linear-gradient(
    to right,
    rgba(0, 84, 153, 1) 0%,
    rgba(48, 121, 189, 1) 100%
  );
  filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#005499', endColorstr='#3079bd', GradientType=1 );
}
.outgoing-msg::before {
  display: block;
  position: absolute;
  top: -10px;
  right: -8px;
  content: "";
  width: 0;
  height: 0;
  border-right: 10px solid transparent;
  border-top: 10px solid transparent;
  border-left: 10px solid rgba(48, 121, 189, 1);
  border-bottom: 10px solid transparent;
  transform: rotate(-135deg);

  border-radius: 5px;
}
</style>