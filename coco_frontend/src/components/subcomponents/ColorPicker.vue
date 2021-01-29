<template>
  <div>
    <v-bottom-sheet v-model="sheet">
      <v-sheet class="text-center" height="220px">
        <v-container>
          <v-row align="center">
            <v-col>
              <p>Entrantes</p>
              <v-color-picker
                v-model="incomingColor"
                class="ma-2"
                dot-size="24"
                hide-canvas
                hide-mode-switch
                mode="hexa"
                swatches-max-height="250"
              ></v-color-picker>
            </v-col>
            <v-col>
              <p>Salientes</p>
              <v-color-picker
                v-model="outgoingColor"
                class="ma-2"
                dot-size="24"
                hide-canvas
                hide-mode-switch
                mode="hexa"
                swatches-max-height="250"
              ></v-color-picker>
            </v-col>
            <v-col>
              <p>Fondo</p>
              <v-color-picker
                v-model="bgColor"
                class="ma-2"
                dot-size="24"
                hide-canvas
                hide-mode-switch
                mode="hexa"
                swatches-max-height="250"
              ></v-color-picker>
            </v-col>
            <v-btn color="primary darken-3" @click="resetColors"
              >Reestablecer</v-btn
            >
          </v-row>
          <v-col></v-col>
        </v-container>
      </v-sheet>
    </v-bottom-sheet>
  </div>
</template>

<script>
export default {
  name: "ColorPicker",
  props: ["incoming", "outgoing", "bg"],
  data:()=>({
    sheet: false,
  }),
  created(){
    this.sheet = true;
  },
  beforeDestroy(){
    this.sheet = false;
  },
  watch:{
    sheet(){
      this.$emit("sheetStatus", this.sheet)
    }
  },
  computed: {
    incomingColor: {
      get() {
        return this.incoming;
      },
      set(value) {
        this.$emit("incomingColor", value);
      },
    },
    outgoingColor: {
      get() {
        return this.outgoing;
      },
      set(value) {
        this.$emit("outgoingColor", value);
      },
    },
    bgColor: {
      get() {
        return this.bg;
      },
      set(value) {
        this.$emit("bgColor", value);
      },
    },
  },
  methods: {
    resetColors() {
      this.incomingColor = "#09243df5";
      this.outgoingColor = "#3079bdfa";
      this.bgColor = "#3636362a";
    },
  },
};
</script>

<style>
</style>