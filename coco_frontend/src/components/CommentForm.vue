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
          placeholder="Coméntale algo! 😊"
          contenteditable="true"
          :id="'CommentDiv'+barterId"
          @keydown="setComment"
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
        <v-btn class="ml-10" small color="primary darken-3" rounded>
          Comentar
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "CommentForm",
  props: ["barterId"],
  computed: {
    ...mapState(["user"]),
  },
  data: () => ({
    comment: '',
    image: "",
    imgUrl: "",
  }),
  methods: {
    addImage2Comment(img) {
      this.image = img;
      this.imgUrl = URL.createObjectURL(img);
    },
    setComment(){
      let commentDiv = document.getElementById('CommentDiv'+this.barterId);
      this.comment = commentDiv.innerText.trim();
      console.log(this.comment.length)
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
  color: #4a4a4a;
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
  z-index: 10;
}
</style>