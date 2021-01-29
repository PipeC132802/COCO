<template>
  <div>
    <v-bottom-sheet v-model="sheet">
      <v-sheet
        class="text-center"
        :style="smallDevice ? 'overflow-y: auto' : ''"
        max-height="200px"
      >
        <v-container class="pt-1 pb-0">
          <v-row class="pt-0 mb-0" align="center">
            <v-col class="pt-0" cols="12" sm="12" md="3">
              <p>Entrantes</p>
              <v-color-picker
                width="100%"
                v-model="incomingColor"
                class="ma-2"
                dot-size="24"
                hide-canvas
                hide-mode-switch
                mode="hexa"
                swatches-max-height="250"
              ></v-color-picker>
            </v-col>
            <v-col cols="12" sm="12" md="3">
              <p>Salientes</p>
              <v-color-picker
                width="100%"
                v-model="outgoingColor"
                class="ma-2"
                dot-size="24"
                hide-canvas
                hide-mode-switch
                mode="hexa"
                swatches-max-height="250"
              ></v-color-picker>
            </v-col>
            <v-col cols="12" sm="12" md="3">
              <p>Fondo</p>
              <v-color-picker
                width="100%"
                v-model="bgColor"
                class="ma-2"
                dot-size="24"
                hide-canvas
                hide-mode-switch
                mode="hexa"
                swatches-max-height="250"
              ></v-color-picker>
            </v-col>
            <v-col cols="12" sm="12" md="3" class="text-center">
              <v-btn
                :block="smallDevice"
                color="primary darken-3"
                @click="resetColors"
                >Reestablecer</v-btn
              >
            </v-col>
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
  data: () => ({
    sheet: false,
    smallDevice: false,
  }),
  created() {
    this.sheet = true;
    let width = window.screen.width;
    if (width <= 920) {
      this.smallDevice = true;
    } else {
      this.smallDevice = false;
    }
  },
  
  beforeUpdate() {},
  watch: {
    sheet() {
      this.$emit("sheetStatus", this.sheet);
    },
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
#bottom-sheet {
  display: block;
}
#navigation-picker {
  display: none;
}
@media (min-width: 920px) {
  #navigation-picker {
    display: block;
  }
  #bottom-sheet {
    display: none;
  }
}
</style>