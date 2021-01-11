    <template>
  <v-container class="ma-0 pa-0">
    <v-card-title class="pl-0"> Edita tu comentario </v-card-title>
    <v-row class="px-3 mr-2">
      <v-avatar color="secondary" size="40">
        <v-img v-if="user.profile_picture" :src="user.profile_picture"> </v-img>
        <span v-else class="white--text">{{ user.name.slice(0, 1) }}</span>
      </v-avatar>
      <v-col class="pt-0 form">
        <div
          class="comment"
          contenteditable="true"
          :id="'CommentDiv' + comment.id"
          @keydown="setComment"
        >
          {{ comment.comment }}
        </div>
        <v-img
          max-width="250"
          class="ml-3 mt-1 mb-2 image-in-comment"
          v-if="(comment.photo && !trigger) || imgUrl.length"
          :src="trigger ? imgUrl : comment.photo"
        >
          <v-row>
            <v-btn
              @click="clearImgData()"
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
      <v-col v-if="commentText || image" cols="12">
        <v-btn
          @click="submitComment"
          class="ml-10"
          color="primary darken-3"
          rounded
          :loading="loading"
        >
          Editar
        </v-btn>
      </v-col>
    </v-row>
    <v-snackbar v-model="snackbar">
      {{ message }}
      <template v-slot:action="{ attrs }">
        <v-btn color="error" text v-bind="attrs" @click="snackbar = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

    <script>
import { mapState } from "vuex";
export default {
  name: "CommentForm",
  props: ["commentObj"],
  computed: {
    ...mapState(["user"]),
  },
  data: () => ({
    commentText: "",
    image: "",
    apiDir: "barter-comments/",
    loading: false,
    trigger: false,
    message: "Debes añadir información.",
    snackbar: false,
  }),
  computed: {
    ...mapState(["baseUrl", "user", "authentication"]),
    comment: function () {
      return this.commentObj;
    },
    imgUrl: {
      get: function () {
        if (this.image) return URL.createObjectURL(this.image);
        else return "";
      },
      set: function (val) {
          this.$emit('commentUpdated')
      },
    },
  },
  methods: {
    addImage2Comment(img) {
      this.image = img;
      this.trigger = true;
    },
    setComment() {
      let commentDiv = document.getElementById("CommentDiv" + this.comment.id);
      this.commentText = commentDiv.innerText.trim();
    },
    submitComment() {
      if (this.commentText || this.image) {
        console.log(this.commentText)
        this.loading = true;
        const formData = new FormData();
        formData.append("comment", this.commentText);
        formData.append("action", 1);
        formData.append("commentId", this.comment.id);
        formData.append("photo", this.image);
        let headers = {
          Authorization: `Token ${this.authentication.accessToken}`,
        };
        delete headers["Content-Type"];
        fetch(this.baseUrl + this.apiDir, {
          method: "PUT",
          headers: headers,
          body: formData,
        })
          .then((response) => response.json())
          .then((response) => {
            let commentDiv = document.getElementById(
              "CommentDiv" + this.comment.id
            );
            this.commentText = "";
            this.image = "";
            this.imgUrl = "";
            commentDiv.innerText = "";
            this.$emit("commentPosted");
            this.$root.$emit("reaction", {
              barter: this.comment.id,
              reaction: null,
            });
          })
          .catch((err) => console.error(err))
          .finally(() => {
            this.loading = false;
          });
      } else {
        this.snackbar = true;
      }
    },
    clearImgData() {
      this.trigger = true;
      console.log(this.trigger);
      this.image = "";
    },
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