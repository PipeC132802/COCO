<template>
  <div>
    <v-container v-if="reviews.length" fluid>
      <ReviewsOverview />
    </v-container>
    <v-alert class="mt-3" color="primary darken-3" v-if="!reviews.length" dark icon="mdi-star-off" dense>
      <span
        v-if="user.username == $route.params.username"
      >
        Aún no tienes reseñas 🤨
      </span>
      <span
        v-else-if="!reviews.length && user.username != $route.params.username"
      >
        @{{ $route.params.username }} aún no tiene reseñas 🤨
      </span>
    </v-alert>

    <v-container fluid>
      <v-progress-circular
        v-if="loading"
        class="mt-3 mx-auto"
        size="40"
        color="primary"
        indeterminate
      ></v-progress-circular>
      <v-card
        elevation="3"
        class="mb-2"
        outlined
        v-else
        v-for="review in reviews"
        :key="review.id"
      >
        <v-list class="pb-0 mb-0" subheader two-line>
          <v-list-item class="px-2 mb-0">
            <v-list-item-avatar size="30" color="secondary">
              <v-img
                v-if="review.user_from.profile_profile"
                :src="review.user_from.profile_profile"
              ></v-img>
              <span class="white--text" v-else>{{
                review.user_from.name.slice(0, 1).toUpperCase()
              }}</span>
            </v-list-item-avatar>
            <v-list-item-content class="mt-0 pa-0" style="line-heigth: 1">
              <v-list-item-title :title="review.user_from.name">
                <router-link
                  class="title--text link"
                  :to="{
                    name: 'Profile',
                    params: { username: review.user_from.username },
                  }"
                  >{{ review.user_from.name }}</router-link
                >

                <span
                  class="grey--text ml-2"
                  :title="'@' + review.user_from.username"
                  >@{{ review.user_from.username }}</span
                >
              </v-list-item-title>
              <v-list-item-subtitle>
                <v-icon class="mr-1" small>mdi-clock</v-icon>
                <small :title="timeSince(review.created) | capitalize">{{
                  timeSince(review.created) | capitalize
                }}</small>
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-card-text class="pa-0 ma-0 ml-2 pl-12 pr-5">
            <v-row
              align="center"
              class="px-3"
              :title="review.responsibility + ' estrellas'"
            >
              <span class="grey--text mr-1"> Responsabilidad </span>
              <v-icon
                v-for="i in review.responsibility"
                :key="i"
                small
                color="warning"
                >mdi-star</v-icon
              >
            </v-row>
            <v-row
              align="center"
              class="px-3"
              :title="review.respect + ' estrellas'"
            >
              <span class="grey--text mr-1"> Respeto </span>
              <v-icon v-for="i in review.respect" :key="i" small color="warning"
                >mdi-star</v-icon
              >
            </v-row>
            <v-row
              align="center"
              class="px-3"
              :title="review.communication + ' estrellas'"
            >
              <span class="grey--text mr-1"> Comunicación </span>
              <v-icon
                v-for="i in review.communication"
                :key="i"
                small
                color="warning"
                >mdi-star</v-icon
              >
            </v-row>
            <p v-if="review.opinion" class="mt-3 review-opinion">
              {{ review.opinion }}
            </p>
          </v-card-text>
          <v-divider class="mt-1"></v-divider>
        </v-list>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import moment from "moment";
import ReviewsOverview from "../components/ReviewsOverview";
import { mapState } from "vuex";
export default {
  name: "ReviewsList",
  components: {
    ReviewsOverview,
  },
  data: () => ({
    reviews: [],
    apiDir: "reviews/",
    loading: false,
  }),
  computed: {
    ...mapState(["user", "authentication", "baseUrl"]),
  },
  mounted() {
    this.getReviews();
  },
  methods: {
    getReviews() {
      this.loading = true;
      fetch(this.baseUrl + this.apiDir + `?user=${this.$route.params.username}`)
        .then((response) => response.json())
        .then((response) => (this.reviews = response))
        .catch((err) => console.error(err))
        .finally(() => {
          this.loading = false;
        });
    },
    timeSince(date) {
      let timeSince = moment(date).locale("es").fromNow();
      return timeSince;
    },
  },
};
</script>

<style scoped>
p {
  font-size: 14pt;
  color: rgb(59, 59, 59);
}
.link {
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}
.review-opinion {
  font-size: 16pt;
  color: rgb(73, 73, 73);
}
</style>