<template>
  <div v-if="!authentication.userIsAuthenticated">
    <video-bg />
    <div class="information text-center">
      <h1>¿Crees posible el trueque de habilidades y conocimientos?</h1>
      <p class="mt-2 mb-0">
        En <span class="primary--text"><strong>COCO</strong></span> sí.
      </p>
      <p class="pt-0">¡Únete a COCO hoy mismo!</p>
    </div>
    <v-footer class="footer" color="transparent" dark padless>
      <v-card
        flat
        tile
        min-width="100%"
        color="transparent"
        class="white--text text-center"
      >
        <v-card-text>
          <v-btn
            v-for="socialbtn in social"
            :key="socialbtn.icon"
            class="mx-4 white--text"
            icon
            :href="socialbtn.link"
            target="_blank"
          >
            <v-icon size="24px">
              {{ socialbtn.icon }}
            </v-icon>
          </v-btn>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-text class="white--text">
          <span>© {{ new Date().getFullYear() }} COCO.</span>
        </v-card-text>
      </v-card>
    </v-footer>
  </div>
</template>

<script>
import {addMetaTagData} from "../functions.js";
import { mapState } from "vuex";
import VideoBg from "../components/VideoBg.vue";
import DiscoverHowItWorks from "../components/DiscoverHowItWorks.vue";
export default {
  name: "Welcome",
  components: {
    VideoBg,
    DiscoverHowItWorks,
  },
  data: () => ({
    social: [
      {
        icon: "mdi-facebook",
        link: "https://www.facebook.com/Coco-Platform-111091337351773",
      },
      { icon: "mdi-twitter", link: "https://twitter.com/coco_platform" },
      { icon: "mdi-instagram", link: "https://instagram.com/coco_platform" },
    ],
  }),
  created() {},
  computed: {
    ...mapState(["authentication", "userRequireMoreInfo"]),
  },
  created() {
    if (!this.userRequireMoreInfo) {
      this.$router.push({ name: "MoreInfo" });
    }
    if (this.authentication.userIsAuthenticated) {
      this.$router.push({ name: "Home" });
    }
    document.title = "Comparte tus conocimientos en COCO";
    let metaObj = [
        {property: 'og:title', content: "'Truequea' tus conocimientos con COCO"},
        {property: 'og:description', content: "Busca personas con conocimientos en lo que quieres aprender e interés en lo que sabes. ¡Truequea tus habilidades!"},
        {property: 'description', content: "Busca personas con conocimientos en lo que quieres aprender e interés en lo que sabes. ¡Truequea tus habilidades!"},
        {property: 'title', content: "'Truequea' tus conocimientos con COCO"},
      ];
      addMetaTagData(metaObj);
  },
  mounted() {
    let btn = document.getElementsByClassName("logo-btn");
    btn.forEach((element) => {
      element.classList.remove("v-list-item--active");
    });
    this.$root.$emit("toolBarColor", "transparent");
  },
  beforeDestroy() {
    this.$root.$emit("toolBarColor", "white");
  },
  methods: {},
};
</script>
<style>
.information {
  position: relative;
  color: white;
  font-size: calc(0.8vw + 0.8em);
  width: 100%;
  height: auto;
  margin: 25vh auto 0px auto;
  z-index: 2;
}
.footer {
  z-index: 1;
  margin-top: 10%;
}
</style>