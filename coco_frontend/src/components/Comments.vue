<template>
  <v-container
    v-if="(comments.length || user.username != $route.params.username) && authentication.userIsAuthenticated"
    class="ma-0 pt-0 px-0"
  >
    <CommentForm
      v-on:commentPosted="getComments"
      v-if="author != user.username"
      :barterId="barterId"
    />
    <div class="pl-1 pr-4" v-if="comments.length">
      <p title="Más recientes" class="recents mt-4 mb-0 pb-0">Más recientes</p>
      <v-list
        v-for="comment in comments"
        :key="comment.id"
        class="pb-0 mb-0"
        subheader
        two-line
        :id="'comment_'+comment.id"
      >
        <v-list-item class="px-2 mb-0">
          <v-list-item-avatar size="30" color="secondary">
            <v-img
              v-if="comment.user.profile_picture"
              :src="comment.user.profile_picture"
            ></v-img>
            <span class="white--text" v-else>{{
              comment.user.name.slice(0, 1).toUpperCase()
            }}</span>
          </v-list-item-avatar>
          <v-list-item-content class="mt-0 pa-0" style="line-heigth: 1">
            <v-list-item-title :title="comment.user.name">
              <router-link
                class="title--text"
                :to="{
                  name: 'Profile',
                  params: { username: comment.user.username },
                }"
                >{{ comment.user.name.trim() }}</router-link
              >

              <span class="grey--text ml-2" :title="'@' + comment.user.username"
                >@{{ comment.user.username }}</span
              >
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-icon class="mr-1" small>mdi-clock</v-icon>
              <small :title="timeSince(comment.created) | capitalize">{{
                timeSince(comment.created) | capitalize
              }}</small>
              
              <span
                v-if="user.username == author && !comment.accepted"
                class="success--text ml-2 accept-action"
                @click="acceptProposal(comment)"
                title="Aceptar"
                >Aceptar</span
              >
              <span title="Aceptada" class="white--text primary accepted ml-2" v-else-if="comment.accepted">Aceptada</span>
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action class="pr-4">
            <v-menu
              top
              open-on-hover
              offset-y
              bottom
              transition="slide-y-transition"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn dark icon v-bind="attrs" v-on="on">
                  <v-icon color="grey darken-3">mdi-dots-horizontal</v-icon>
                </v-btn>
              </template>
              
              <v-list v-if="comment.user.username == user.username" class="pa-0">
                <v-list-item
                  class="item-menu pl-1"
                  v-for="(item, i) in items.self"
                  :key="i"
                  @click="setEvent(item.title, comment)"
                >
                  <v-list-item-title>
                    <v-icon class="ml-1" left>{{ item.icon }}</v-icon>
                    {{ item.title }}</v-list-item-title
                  >
                </v-list-item>
              </v-list>
              <v-list v-else class="pa-0">
                <v-list-item
                  class="item-menu pl-1"
                  v-for="(item, i) in items.other"
                  :key="i"
                >
                  <v-list-item-title>
                    <v-icon class="ml-1" left>{{ item.icon }}</v-icon>
                    {{ item.title }}</v-list-item-title
                  >
                </v-list-item>
              </v-list>
            </v-menu>
          </v-list-item-action>
        </v-list-item>
        <v-card-text class="pa-0 ma-0 ml-2 pl-12 pr-5">
          {{ comment.comment }}
          <v-img
            v-if="comment.photo"
            :src="comment.photo"
            max-width="250"
          ></v-img>
        </v-card-text>
        <v-divider class="mt-1"></v-divider>
      </v-list>
    </div>
    <ProposalAccepted v-on:messageSent="chatData = ''; proposal=false;" v-if="proposal" :chatData="chatData" />
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import { sendNotificationViaWS } from "../functions.js";
import moment from "moment";
import CommentForm from "../components/CommentForm.vue";
import ProposalAccepted from "../components/ProposalAccepted.vue";
export default {
  name: "Comments",
  props: ["barterId", "author"],
  components: {
    CommentForm,
    ProposalAccepted
  },
  data: () => ({
    comments: [],
    apiDir: "barter-comments/",
    items: {
      self: [{ title: "Eliminar", icon: "mdi-delete" }],
      other: [{ title: "Reportar", icon: "mdi-alert" }],
    },
    comment2Edit: "",
    commentDialog: false,
    chatData:'',
    proposal: false,
  }),
  computed: {
    ...mapState(["user", "authentication", "baseUrl", "wsBase"]),
  },
  beforeUpdate() {
    if (this.commentDialog == false) {
      this.comment2Edit = "";
    }
  },
  mounted() {
    this.getComments();
  },
  methods: {
    getComments() {
      fetch(this.baseUrl + this.apiDir + `?barter=${this.barterId}`, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          this.comments = response;
        })
        .catch((err) => console.error(err));
    },
    timeSince(date) {
      let timeSince = moment(date).locale("es").fromNow();
      return timeSince;
    },
    setEvent(title, comment) {
      if ((title = "Eliminar")) {
        this.deleteComment(comment);
      }
    },
    deleteComment(comment) {
      fetch(this.baseUrl + this.apiDir + `?comment=${comment.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          this.getComments();
        })
        .catch((err) => console.error(err));
    },
    acceptProposal(comment) {
      let formData = {
        comment: comment.id,
        action: 'accept'
      } 
      fetch(this.baseUrl + this.apiDir, {
        method: "PUT",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
        .then((response) => response.json())
        .then((response) => {
          this.notifyUser(response)
          this.getComments();
          this.proposal = true;
          this.chatData = {
            sender : this.user,
            receiver : comment.user,
            conversation : response.conversation
          }
        })
        .catch((err) => console.error(err))
        
    },
     notifyUser(response) {
        let sockedData = {
          type: "new_notification",
          sender: this.user.username,
          receiver: response.user_comment,
          userFrom: response.user_accept,
          action: response.action,
          barter: response.barter,
          field: response.field,
          comment: response.comment,
          created: response.created,
        };
        sendNotificationViaWS(sockedData, this.wsBase, sockedData.receiver);
      }
  },
};
</script>

<style scoped>
.recents {
  font-size: 11pt;
  font-weight: bold;
}
.accept-action:hover {
  text-decoration: underline;
  cursor: pointer;
}
.v-list-item__action {
  z-index: 100;
}
.item-menu:hover {
  background: rgb(219, 219, 219);
  cursor: pointer;
}
a {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
.accepted{
  font-size: 10pt;
  padding: 5px;
  letter-spacing: 0.5px;
  border-radius: 30%;
}
:target {
  background: rgba(185, 185, 185, 0.61);
  border-radius: 5px;
}
</style>