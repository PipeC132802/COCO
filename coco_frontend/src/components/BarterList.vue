
<template>
  <div class="mt-5">
    <div v-if="!loaded">
      <v-skeleton-loader
        v-for="index in 10"
        :key="index"
        type="list-item-avatar-two-line, article"
      ></v-skeleton-loader>
    </div>
    <v-card
      elevation="5"
      class="mb-4"
      v-for="barter in barters"
      :key="barter.id"
    >
      <v-divider></v-divider>
      <v-list subheader three-line>
        <v-list-item>
          <v-list-item-avatar>
            <v-img
              v-if="barter.user.profile_picture"
              :src="barter.user.profile_picture"
            ></v-img>
            <span v-else>{{ barter.user.name.slice(0, 1).toUpperCase() }}</span>
          </v-list-item-avatar>
          <v-list-item-content class="mt-0" style="line-heigth: 1">
            <v-list-item-title :title="barter.user.name"
              >{{ barter.user.name }}
              <span class="grey--text" :title="'@' + barter.user.username"
                >@{{ barter.user.username }}</span
              >
              ·
              <small :title="timeSinceShort(barter.created) | capitalize">{{
                timeSinceShort(barter.created) | capitalize
              }}</small>
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-card-title class="ma-0 pa-0">
                {{ barter.title }}
              </v-card-title>
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>
            <v-menu
              top
              open-on-hover
              offset-y
              bottom
              transition="slide-y-transition"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn dark icon v-bind="attrs" v-on="on">
                  <v-icon color="grey darken-3">mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list class="pa-0">
                <v-list-item
                  class="item-menu pl-1"
                  v-for="(item, i) in items"
                  :key="i"
                >
                  <v-list-item-title>
                    <v-icon class="ml-1" left>{{ item.icon }}</v-icon>
                    {{ item.title }}</v-list-item-title
                  >
                </v-list-item>
              </v-list>
            </v-menu>
          </v-list-item-action>
        </v-list-item>
        <v-card-subtitle class="pa-0 pt-0 mx-4">
          <v-chip :title="'Enseñaré ' + barter.skill" color="primary darken-1">
            <v-icon class="pl-1" small pill left> mdi-teach </v-icon>
            {{ barter.skill }}
          </v-chip>
          <v-chip
            :title="'Quiero aprender ' + barter.interest"
            class="ml-3"
            color="accent darken-1"
          >
            <v-icon class="pl-1" small pill left> mdi-school </v-icon>
            {{ barter.interest }}
          </v-chip>
          <v-chip :title="'🌎'+barter.about.place" class="ml-3" label>
            <v-icon small left>mdi-map-marker</v-icon>
            {{ barter.about.place }}
          </v-chip>
        </v-card-subtitle>
        <v-card-text class="px-4 mt-3">
          <p>
            {{ barter.about.description }}
          </p>
        </v-card-text>
      </v-list>
    </v-card>
  </div>
</template>


<script>
import { mapState } from "vuex";
import moment from "moment";
export default {
  name: "BarterList",
  props: ["field"],
  data: () => ({
    items: [
      { title: "Editar", icon: "mdi-pencil" },
      { title: "Eliminar", icon: "mdi-delete" },
      { title: "Reportar", icon: "mdi-alert" },
    ],
    apiDir: "barter-list-api/",
    barters: "",
    loaded: false,
  }),
  computed: {
    ...mapState(["baseUrl", "user"]),
  },
  created() {
    this.fetchBarterList();
  },
  methods: {
    fetchBarterList() {
      fetch(
        this.baseUrl +
          this.apiDir +
          `?username=${this.getUsername()}&field=${this.field}`
      )
        .then((response) => response.json())
        .then((response) => {
          this.barters = response;
          this.loaded = true;
        });
    },
    getUsername() {
      let username = "";
      username = this.$route.params.username;
      if (username == undefined) {
        username = this.user.username;
      }
      return username;
    },
    timeSinceShort(date) {
      let timeSince = moment(date).locale("es").fromNow();
      return timeSince;
    },
  },
  filters: {
    capitalize: function (value) {
      if (!value) return "";
      value = value.toString();
      return value.charAt(0).toUpperCase() + value.slice(1);
    },
  },
};
</script>

<style  scoped>
.item-menu:hover {
  background: rgb(219, 219, 219);
  cursor: pointer;
}
p {
  font-size: 14pt;
  color: rgb(59, 59, 59);
}
</style>

