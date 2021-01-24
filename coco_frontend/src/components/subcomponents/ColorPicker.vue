<template>
  <div>
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
        <v-btn color="primary darken-3" @click="resetColors">Reestablecer</v-btn>
      </v-row>
      <v-col></v-col>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "ColorPicker",
  props: ["incoming", "outgoing", "bg"],
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
  methods:{
      resetColors(){
          this.incomingColor = '#f06b24fb'
          this.outgoingColor = '#3079bdfa'
          this.bgColor = '#3636362a';
      }
  }
};
</script>

<style>
</style>