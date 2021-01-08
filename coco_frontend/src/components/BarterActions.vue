    <template>
  <v-container class="ma-0 pt-0" fluid>
    <v-row>
      <v-hover v-slot="{ hover }">
        <v-btn text class="mr-1">
          <v-icon left small> mdi-thumb-up </v-icon>

          Reaccionar
          <v-expand-transition>
            <v-card
              v-if="hover"
              class="d-flex transition-fast-in-fast-out v-card--reveal reactions-box px-2"
              elevation="12"
              rounded="pill"
            >
              <v-row justify="space-around" class="px-3 pt-1">
                <span data-title="Cool" class="reaction"> 😎 </span>
                <span data-title="Genial" class="reaction"> 🤩 </span>
                <span data-title="Interesante" class="reaction"> 🤔 </span>
                <div>
                  {{ title }}
                </div>
              </v-row>
            </v-card>
          </v-expand-transition>
        </v-btn>
      </v-hover>

      <v-btn text class="mr-1">
        <v-icon left small> mdi-comment-text-multiple </v-icon>
        Comentar
      </v-btn>
      <v-btn text>
        <v-icon left small> mdi-share-variant </v-icon>
        Compartir
      </v-btn>
    </v-row>
  </v-container>
</template>

    <script>
export default {
  name: "BarterActions",
  props: ["barterId"],
  data: () => ({
    title: "",
  }),
  methods: {},
};
</script>

    <style>
.reactions-box {
  position: absolute;
  top: -50px;
  left: -10px;
  height: 30pt;
  width: 200px;
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
  left: -50%;
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
</style>