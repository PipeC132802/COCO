<template>
  <div>
    <v-card elevation="3" outlined>
      <v-row align="center">
        <v-col class="text-center pb-0 mb-0" cols="12" sm="12" md="6" >
          <div>
            <p class="display-2 mb-0">{{ overview.average.toFixed(2) }}</p>
            <v-icon color="primary" v-for="i in stars" :key="i">
              mdi-star
            </v-icon>
            <p>
              <small class="grey--text mt-2"
                >Promedio entre {{ overview.total }}
                {{ "reseña" + pluralize(overview.total) }}</small
              >
            </p>
          </div>
        </v-col>
        <v-col cols="12" sm="12" md="6" class="text-center pa-0 px-3 mt-0">
          <v-container class="pa-0 px-3" fluid>
            <v-row dense>
              <v-col><small>Responsabilidad</small></v-col>
              <v-col>
                <v-progress-linear
                  class="mt-3"
                  :value="getPorcentage(overview.responsibility)"
                ></v-progress-linear>
              </v-col>
              <v-col>
                <small
                  >{{ overview.responsibility }}
                  {{ "estrella" + pluralize(overview.responsibility) }}</small
                >
              </v-col>
            </v-row>
            <v-row dense>
              <v-col><small>Respeto</small></v-col>
              <v-col>
                <v-progress-linear
                  class="mt-3"
                  :value="getPorcentage(overview.respect)"
                ></v-progress-linear>
              </v-col>
              <v-col>
                <small
                  >{{ overview.respect }}
                  {{ "estrella" + pluralize(overview.respect) }}</small
                >
              </v-col>
            </v-row>
            <v-row dense>
              <v-col><small>Comunición</small></v-col>
              <v-col>
                <v-progress-linear
                  class="mt-3"
                  :value="getPorcentage(overview.communication)"
                ></v-progress-linear>
              </v-col>
              <v-col>
                <small
                  >{{ overview.communication }}
                  {{ "estrella" + pluralize(overview.communication) }}</small
                >
              </v-col>
            </v-row>
          </v-container>
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
    stars: function () {
      return Math.round(this.overview.average);
    },
  },
  mounted() {
    this.getReviewsOverview();
  },
  methods: {
    getReviewsOverview() {
      fetch(this.baseUrl + this.apiDir + `?user=${this.$route.params.username}`)
        .then((response) => response.json())
        .then((response) => {
          this.overview = response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    pluralize: function (val) {
      if (val > 1 || val == 0) {
        return "s";
      } else {
        return "";
      }
    },
    getPorcentage(val) {
      return (val / 5) * 100;
    },
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