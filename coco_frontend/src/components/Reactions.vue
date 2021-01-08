<template>
  <div>
    <v-container fluid class="ma-0 pt-0">
      <v-row class="ma-0 pa-0 verbose">
        <div v-if="reactionsTypes.length" class="mr-1">
          {{ reactionsEmojis }}
        </div>
        <span>
          {{ reactionsVerbose }}
        </span>

        <span class="mx-1">•</span>
        <p class="ma-0 verbose comments">{{ commentsVerbose }}</p>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Reactions.vue",
  props: ["barterId"],
  data: () => ({
    reactionsCount: 0,
    reactionsTypes: [],
    comments: 0,
    apiDir: "barter-reactions/",
  }),
  mounted() {
    this.$root.$on("reaction", (data) => {
      if(data.barter === this.barterId){
       this.getReactions();
      }
    });
  },

  computed: {
    ...mapState(["baseUrl"]),
    reactionsEmojis: function () {
      let emojis = "";
      this.reactionsTypes.forEach((type) => {
        switch (type) {
          case 1:
            emojis += "😎";
            break;
          case 2:
            emojis += "🤩";
            break;
          case 3:
            emojis += "🤔";
            break;

          default:
            break;
        }
      });
      return emojis;
    },
    reactionsVerbose: function () {
      let string = "";
      if (this.reactionsCount > 1 || this.reactionsCount == 0) {
        string = this.reactionsCount + " reacciones";
      } else {
        string = "Una reacción";
      }
      return string;
    },
    commentsVerbose: function () {
      let string = "";
      if (this.comments > 1 || this.comments == 0) {
        string = this.comments + " propuestas";
      } else {
        string = "Una propuesta";
      }
      return string;
    },
  },
  created() {
    this.getReactions();
  },
  methods: {
    getReactions() {
      fetch(this.baseUrl + this.apiDir + `?barter_id=${this.barterId}`)
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.reactionsCount = response.reactions;
          this.reactionsTypes = response.types;
          this.comments = response.comments;
        });
    },
  },
};
</script>

<style>
.verbose {
  font-size: 10pt;
}
.comments:hover {
  color: #307abd;
  cursor: pointer;
  text-decoration: underline;
}
</style>