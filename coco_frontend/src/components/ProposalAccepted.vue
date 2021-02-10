<template>
  <div>
    <v-dialog persistent max-width="500" v-model="dialog">
      <v-card>
        <v-card-title class="pb-0">
          <v-list two-line>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  Para:
                  <v-chip color="primary">
                    <v-avatar color="secondary" left>
                      <v-img
                        v-if="chatData.receiver.profile_picture"
                        :src="chatData.receiver.profile_picture"
                      ></v-img>
                      <span v-else class="white--text">{{
                        chatData.receiver.name.slice(0, 1)
                      }}</span>
                    </v-avatar>
                    {{ chatData.receiver.name }}</v-chip
                  >
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-divider></v-divider>
          </v-list>
        </v-card-title>
        <v-card-text>
          <v-textarea
            outlined
            v-model="message"
            name="input-7-4"
            label="Mensaje"
          ></v-textarea>

          <v-row class="px-3 mt-0">
            <v-btn
              class="ml-auto"
              @click="sendMessage"
              color="primary darken-2"
              :loading="loading"
            >
              <v-icon left>mdi-send</v-icon>
              Enviar
            </v-btn>
          </v-row>
        </v-card-text>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar">
      {{ snackMsg }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import { mapState } from "vuex";
import { encrypt, sendNotificationViaWS } from "@/functions.js";
export default {
  name: "ProposalAccepted",
  props: ["chatData"],
  data: () => ({
    dialog: false,
    message: "",
    loading: false,
    apiDir: "messages/",
    snackbar: false,
    snackMsg: "",
  }),
  computed: {
    ...mapState(["authentication", "baseUrl", "wsBase"]),
  },
  mounted() {
    this.dialog = true;
    this.message = `Hola ${this.chatData.receiver.name.trim()}, acepté tu propuesta ya que me parece interesante y me gustaría acordar los horarios para realizar nuestro trueque.`;
  },
  methods: {
    sendMessage() {
      if (this.message.trim()) {
        let formData = {
          owner: this.chatData.sender.username,
          opponent: this.chatData.receiver.username,
          text: encrypt(this.message.trim(), this.chatData.sender.username),
        };
        fetch(this.baseUrl + this.apiDir, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Token ${this.authentication.accessToken}`,
          },
          body: JSON.stringify(formData),
        })
          .then((response) => {
            if (response.status == 200) {
              this.snackMsg = "Mensaje enviado!";
              this.snackbar = true;
              this.dialog = false;
              this.$emit("messageSent");
              let sockedData = {
                type: "new_msg",
                sender: this.chatData.sender.username,
                receiver: this.chatData.receiver.username,
              };
              sendNotificationViaWS(
                sockedData,
                this.wsBase,
                sockedData.receiver
              );
            } else {
              throw new Error();
            }
          })
          .catch((err) => {
            this.snackMsg = "Ha sucedido un error inesperado.";
            this.snackbar = true;
          })
          .finally(() => {
            this.loading = false;
          });
      } else {
        this.snackMsg = "Debes agregar un mensaje";
        this.snackbar = true;
      }
    },
  },
};
</script>

<style>
</style>