<template>
  <v-container class="ma-0 pa-0">
    <v-row class="px-3 mr-2">
      <v-avatar color="secondary" size="40">
        <v-img v-if="user.profile_picture" :src="user.profile_picture"> </v-img>
        <span v-else class="white--text">{{ user.name.slice(0, 1) }}</span>
      </v-avatar>
      <v-col class="pt-0 form">
        <div
          class="comment"
          placeholder="Propónle algo! 😊"
          contenteditable="true"
          :id="'CommentDiv' + barterId"
          @keyup="setComment"
        ></div>
        <v-img
          max-width="250"
          class="ml-3 mt-1 mb-2 image-in-comment"
          v-if="image"
          :src="imgUrl"
        >
          <v-row>
            <v-btn
              @click="
                imgUrl = '';
                image = '';
              "
              title="Quitar foto"
              color="primary darken-3"
              class="mr-4 mt-1 ml-auto"
              fab
              small
            >
              <v-icon> mdi-delete </v-icon>
            </v-btn>
          </v-row>
        </v-img>

        <v-row class="comment-actions">
          <v-btn icon>
            <v-icon> mdi-image </v-icon>
          </v-btn>
          <v-file-input
            @change="addImage2Comment"
            class="image-input"
            accept="image/png, image/jpeg, image/bmp"
          ></v-file-input>
        </v-row>
      </v-col>
      <v-col v-if="comment || image" cols="12">
        <v-btn
          @click="submitComment"
          class="ml-10"
          small
          color="primary darken-3"
          rounded
          :loading="loading"
        >
          Proponer
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import { sendNotificationViaWS } from "../functions.js";

export default {
  name: "CommentForm",
  props: ["barterId"],
  computed: {
    ...mapState(["user"]),
  },
  data: () => ({
    comment: "",
    image: "",
    imgUrl: "",
    apiDir: "barter-comments/",
    loading: false,
  }),
  computed: {
    ...mapState(["baseUrl", "user", "authentication","wsBase"]),
  },
  methods: {
    addImage2Comment(img) {
      this.image = img;
      this.imgUrl = URL.createObjectURL(img);
    },
    setComment() {
      let commentDiv = document.getElementById("CommentDiv" + this.barterId);
      this.comment = commentDiv.innerText;
    },
    submitComment() {
      if (this.comment.trim().length || this.image) {
        this.loading = true;
        const formData = new FormData();
        formData.append("comment", this.comment);
        formData.append("barter", this.barterId);
        formData.append("photo", this.image);
        let headers = {
          Authorization: `Token ${this.authentication.accessToken}`,
        };
        delete headers["Content-Type"];
        fetch(this.baseUrl + this.apiDir, {
          method: "POST",
          headers: headers,
          body: formData
        })
        .then((response)=>(response.json()))
        .then((response)=>{
          this.notifyUser(response);
          let commentDiv = document.getElementById("CommentDiv" + this.barterId);
          this.comment = '';
          this.image = '';
          this.imgUrl = '';
          commentDiv.innerText = '';
          this.$emit('commentPosted');
          this.$root.$emit("reaction", {
              barter: this.barterId,
              reaction: null,
            });
        })
        .catch((err)=>console.error(err))
        .finally(()=>{
          this.loading = false;

        })
      }
    },
    notifyUser(response) {
        let sockedData = {
          type: "new_notification",
          sender: this.user.username,
          receiver: response.user_barter,
          userFrom: response.user_comment,
          action: response.action,
          barter: response.barter,
          field: response.field,
          comment: response.comment,
          created: response.created,
        };
        sendNotificationViaWS(sockedData, this.wsBase, response.user_barter);
    }
  },
};
</script>

<style>
.comment {
  min-height: 30px;
  overflow: auto;
  outline: transparent;
  word-break: break-word;
  padding-top: 5px;
  margin: 1px 0 5px 15px;
}.comment:hover{
  cursor: text;
}
.image-in-comment {
  border-radius: 2%;
}
.image-input {
  opacity: 0;
  filter: alpha(opacity=0);
  position: absolute;
  max-width: 40px;
  max-height: 35px;
  top: -12px;
}
[contenteditable][placeholder]:empty:before {
  content: attr(placeholder);
  position: relative;
  color: #757575;
  background-color: transparent;
}
.form {
  position: relative;
  border: 2px solid rgb(121, 121, 121);
  border-radius: 20px;
  margin-left: 10px;
  padding: 0 100px 0 0;
}
.comment-actions {
  position: absolute;
  top: 0px;
  right: 20px;
  z-index: 3;
}
</style>