<template>
  <v-container class="ma-0 pa-0">
    <v-row class="px-3 mr-2">
      <v-avatar size="40">
        <v-img v-if="user.profile_picture" :src="user.profile_picture"> </v-img>
        <span v-else class="white--text">{{ user.name.slice(0, 1) }}</span>
      </v-avatar>
      <v-col class="pt-0 form">
        <div
          class="comment"
          placeholder="Haz una propuesta"
          contenteditable="true"
        ></div>

        <v-row class="comment-actions">
          <picker
            v-if="emojiPicker"
            :style="{ position: 'absolute', top: '30px', right: '20px', 'z-index': '100' }"
            set="emojione"
            @select="addEmoji"
            :emoji="emoji"
            :showPreview="false"
            :i18n="i18n"
          />
          <v-btn @click="emojiPicker = !emojiPicker" icon>
            <v-icon> mdi-emoticon-excited-outline </v-icon>
          </v-btn>
          <v-btn icon>
            <v-icon> mdi-image </v-icon>
          </v-btn>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Picker } from "emoji-mart-vue";
import { mapState } from "vuex";
export default {
  name: "CommentForm",
  components: { Picker },
  props: ["barterId"],
  computed: {
    ...mapState(["user"]),
  },
  data: () => ({
    emojiPicker: false,
    emoji:"",
    i18n: {
      search: "Buscar",
      notfound: "No se encontraron emojis",
      categories: {
        search: "Buscar",
        recent: "Frecuentes",
        people: "Personas",
        nature: "Animales y naturaleza",
        foods: "Comidas y bebidas",
        activity: "Actividades",
        places: "Viajes y lugares",
        objects: "Objetos",
        symbols: "Simbolos",
        flags: "Banderas",
        custom: "Personalizados",
      },
    },
  }),
  methods: {
      addEmoji(){
          console.log('s')
      }
  },
};
</script>

<style>
.comment {
  min-height: 30px;
  padding: 5px 100px 0px 15px;
  min-height: 40px;
  max-height: 100px;
  overflow: auto;
  outline: transparent;
  border-radius: 20px;
  border: 2px solid rgb(121, 121, 121);
  word-break: break-word;
}

[contenteditable][placeholder]:empty:before {
  content: attr(placeholder);
  position: relative;
  color: #4a4a4a;
  background-color: transparent;
}
.form {
  position: relative;
}
.comment-actions {
  position: absolute;
  top: 2px;
  right: 30px;
  z-index: 10;
}
</style>