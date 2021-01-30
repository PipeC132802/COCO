    <template>
  <v-container class="pl-1 ma-0 pt-0" fluid>
    <v-row class="btn-actions">
      <v-hover v-slot="{ hover }">
        <v-btn
          :color="getColor"
          class="mr-1 pl-3 action"
          text
          @click="reac2Barter(0)"
        >
          <v-icon v-if="!reaction" small> mdi-thumb-up</v-icon>
          <v-icon small style="font-style: normal" v-else>
            {{ reactionMsg.split(" ")[0] }}
          </v-icon>
          <span class="btn-text ml-1">
          {{ reactionMsg.split(" ")[1] }}
          </span>
          <v-expand-transition>
            <v-card
              v-if="hover"
              class="d-flex transition-fast-in-fast-out v-card--reveal reactions-box mx-1"
              elevation="5"
              rounded="pill"
              min-width="120"
            >
              <v-row justify="space-around" class="pt-1 px-4">
                <span
                  @click="reac2Barter(1)"
                  data-title="Cool"
                  class="reaction"
                >
                  😎
                </span>
                <span
                  @click="reac2Barter(2)"
                  data-title="Genial"
                  class="reaction"
                >
                  🤩
                </span>
                <span
                  @click="reac2Barter(3)"
                  data-title="Interesante"
                  class="reaction"
                >
                  🤔
                </span>
                <div >
                  {{ title }}
                </div>
              </v-row>
            </v-card>
          </v-expand-transition>
        </v-btn>
      </v-hover>

      <v-btn @click="showComments" text class="mr-1 action">
        <v-icon small> mdi-comment-text-multiple </v-icon>
        <span class="btn-text ml-1">

        Proponer
        </span>
      </v-btn>
      <v-btn class="action" text>
        <v-icon small> mdi-share-variant </v-icon>
        <span class="btn-text ml-1">
        Compartir
        </span>
      </v-btn>
    </v-row>
  </v-container>
</template>

    <script>
import { mapState } from "vuex";
import { sendNotificationViaWS } from "../functions.js";
export default {
  name: "BarterActions",
  props: ["barterId"],
  data: () => ({
    title: "",
    reaction: 0,
    reactionMsg: "Reaccionar",
    apiDir: "create-barter-reaction/",
  }),
  computed: {
    ...mapState(["baseUrl", "authentication", "wsBase", "user"]),
    getColor: function () {
      let color = "default";
      switch (this.reaction) {
        case 1:
          color = "primary";
          break;
        case 2:
          color = "success";
          break;
        case 3:
          color = "warning darken-3";
          break;

        default:
          break;
      }
      return color;
    },
  },
  mounted() {
    this.getReaction();
  },
  methods: {
    getReaction() {
      fetch(this.baseUrl + this.apiDir + `?barter_id=${this.barterId}`, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          this.reactionMsg = this.getReactionVerbose(response.reaction);
          this.reaction = response.reaction;
        });
    },
    reac2Barter(reaction) {
      
      var className = event.target.className;
      if (
        (className == "reaction" && reaction) ||
        ((className.indexOf("v-btn") > -1 || className.indexOf("v-icon") > -1 )  && reaction == 0)
      ) {
        let formData = {
          barter_id: this.barterId,
          reaction: reaction,
        };
        fetch(this.baseUrl + this.apiDir, {
          method: "POST",
          headers: {
            Authorization: `Token ${this.authentication.accessToken}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formData),
        })
          .then((response) => response.json())
          .then((response) => {
            this.reactionMsg = this.getReactionVerbose(response.reaction);
            this.reaction = response.reaction;
            this.notifyUser(response);
            this.$root.$emit("reaction", {
              barter: this.barterId,
              reaction: reaction,
            });
          })
          .catch((err) => console.error(err));
      }
    },
    notifyUser(response) {
      if (response.reaction > 0 && response.user_to !== response.user_from.username) {
        let sockedData = {
          type: "new_notification",
          sender: this.user.username,
          receiver: response.user_to,
          reaction: response.reaction,
          userFrom: response.user_from,
          action: response.action,
          barter: response.barter,
          field: response.field,
          created: response.created,
        };
        sendNotificationViaWS(sockedData, this.wsBase, response.user_to);
      }
    },
    showComments() {
      this.$emit("comments", this.barterId);
    },
    getReactionVerbose(reaction) {
      let msg = "";
      switch (reaction) {
        case 1:
          msg = "😎 Cool!";
          break;
        case 2:
          msg = "🤩 Genial!";
          break;
        case 3:
          msg = "🤔 Interesante!";
          break;

        default:
          msg = " Reaccionar";
          break;
      }
      return msg;
    },
  },
};
</script>

    <style>
.reactions-box {
  position: absolute;
  top: -45px;
  left: -15px;
  height: 30pt;
}
.reaction {
  font-size: 16pt;
}
.reaction:hover {
  font-size: 24pt;
}

[data-title]:hover:after {
  opacity: 1;
  transition: all 0.1s ease 0.5s;
  visibility: visible;
}

[data-title]:after {
  content: attr(data-title);
  background-color: rgb(26, 26, 26);
  color: #fff;
  font-size: 10pt;
  position: absolute;

  padding: 5px 20px;
  font-family: Arial, Helvetica, sans-serif;
  top: -30px;
  left: -40%;
  white-space: nowrap;
  box-shadow: 1px 1px 3px #222222;
  opacity: 0;
  z-index: 99999;
  visibility: hidden;
  border-radius: 6px;
  text-transform: capitalize;
}
[data-title] {
  position: relative;
}
.action {
  text-transform: capitalize;
  font-size: calc(1em + 1vw);
}
@media (max-width: 920px) {
  .btn-actions{
    justify-content: start;
    align-items: center;
    padding: 0%;
  }
  .btn-text{
    display: none;
  }
}
</style>