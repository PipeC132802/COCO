<template>
  <div>
    <v-card elevation="3" outlined>
      <v-row class="pt-3">
        <v-col class="text-center">
          <div class="pl-10">
            <p class="display-2 mb-0">{{overview.average.toFixed(2)}}</p>
            <v-icon color="primary" v-for="i in stars" :key="i"> mdi-star </v-icon>
            <p>
              <small class="grey--text mt-2"
                >Promedio entre {{overview.total}} {{'reseña'+pluralize(overview.total)}}</small
              >
            </p>
          </div>
        </v-col>
        <v-col class="mt-2">
          <div class="grid-container">
            <div class="grid-item text-right pr-5">
              <small>Responsabilidad</small>
            </div>
            <div class="grid-item">
              <v-progress-linear class="mt-3" :value="getPorcentage(overview.responsibility)"></v-progress-linear>
            </div>
            <div class="grid-item"><small>{{overview.responsibility}} {{'estrella' + pluralize(overview.responsibility)}}</small></div>

            <div class="grid-item text-right pr-5"><small>Respeto</small></div>
            <div class="grid-item">
              <v-progress-linear class="mt-3" :value="getPorcentage(overview.respect)"></v-progress-linear>
            </div>
            <div class="grid-item"><small>{{overview.respect}} {{'estrella' + pluralize(overview.respect)}}</small></div>

            <div class="grid-item text-right pr-5">
              <small>Comunicación</small>
            </div>
            <div class="grid-item">
              <v-progress-linear class="mt-3" :value="getPorcentage(overview.communication)"></v-progress-linear>
            </div>
            <div class="grid-item"><small>{{overview.communication}} {{'estrella' + pluralize(overview.communication)}} </small></div>
          </div>
        </v-col>
      </v-row>
    </v-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "ReviewsOverview",
  data: () => ({
    overview: {
        average: 0,
    },
    apiDir: "reviews-overview/",
  }),
  computed: {
    ...mapState(["baseUrl"]),
    stars: function(){
        return Math.round(this.overview.average)
    }
  },
  mounted() {
    this.getReviewsOverview();
  },
  methods: {
    getReviewsOverview() {
      fetch(
        this.baseUrl + this.apiDir + `?user=${this.$route.params.username}`
      )
        .then((response) => response.json())
        .then((response) => {this.overview = response})
        .catch((err)=>{console.error(err)})
    },
    pluralize: function (val) {
      if (val > 1 || val == 0) {
        return "s";
      } else {
        return "";
      }
    },
    getPorcentage(val){
        return val / 5 * 100
    }
  },
};
</script>

<style>
.grid-container {
  display: inline-grid;
  grid-template-columns: auto auto auto;
  width: 80%;
  text-align: center;
}
</style>