<template>
  <div>
    <v-container fluid>
      <div class="settings-title">
        <v-btn
          @click="$router.push({ name: 'Account' })"
          class="mr-3"
          icon
          color="primary"
        >
          <v-icon> mdi-arrow-left </v-icon> </v-btn
        >Información de la cuenta
      </div>
      <v-divider></v-divider>
      <v-row align="center">
        <v-col cols="12" class="pt-2">
          <v-list subheader one-line>
            <v-list-item
              v-for="item in info"
              :key="item.title"
              exact
              active-class="primary white--text"
              class="pa-1 px-3 items-info"
            >
              <v-list-item-content>
                <v-list-item-title
                  :title="item.title"
                  v-html="item.title"
                ></v-list-item-title>
                <v-list-item-subtitle :title="item.subtitle">{{
                  !item.subtitle ? "No hay información" : item.subtitle
                }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-col>
        <router-link
          class="link ml-6"
          :to="{ name: 'Edit', params: { username: this.user.username } }"
          >Editar</router-link
        >
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "AccountInfo",
  data: () => ({
    info: [
      { title: "Nombre", subtitle: "" },
      { title: "Usuario", subtitle: "" },
      { title: "Teléfono", subtitle: "" },
      { title: "Lugar", subtitle: "" },
      { title: "Género", subtitle: "" },
      { title: "Edad", subtitle: "" },
    ],
    apiDir: "user-info-update/",
  }),
  computed: {
    ...mapState(["user", "baseUrl", "authentication", "breakpoints"]),
  },
  mounted() {
    this.getUserInfo();
     let screenWidth = window.screen.width;
      if(this.breakpoints.sm > screenWidth){
        this.$emit("main", false)
      } else {
        this.$emit("main", true)
      }
  },
  
  methods: {
    getUserInfo() {
      fetch(this.baseUrl + this.apiDir, {
        method: "GET",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((response) => {
          let birthdatDate = response.birthday
            ? new Date(response.birthday)
            : "";
          let edad = birthdatDate
            ? Math.round(
                (new Date().getTime() - birthdatDate.getTime()) /
                  (1000 * 60 * 60 * 24 * 365)
              )
            : "";
          this.info[0].subtitle =
            response.first_name + " " + response.last_name;
          this.info[1].subtitle = "@" + this.user.username;
          this.info[2].subtitle =
            response.prefix & response.cellphone
              ? response.prefix + response.cellphone
              : "";
          this.info[3].subtitle =
            response.city & response.country
              ? response.city + ", " + response.country
              : "";
          this.info[4].subtitle = response.gender;
          this.info[5].subtitle = edad ? edad + " años" : "";
        });
    },
  },
};
</script>

<style>
.items-info {
  border-bottom: 1px solid rgb(212, 212, 212);
}
.link {
  text-decoration: none;
}
.link:hover {
  text-decoration: underline;
}
</style>