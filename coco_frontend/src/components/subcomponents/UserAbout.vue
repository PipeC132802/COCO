<template>
  <div class="pa-2">
    <v-btn block color="primary" :to="{name:'Edit', params:{username:user.username}}" v-if="!userAbout.bio">Agregar información personal</v-btn>
    <blockquote v-if="userAbout.bio" class="blockquote">
      <p class="mb-0 mt-5 ml-0">
        {{ userAbout.bio }}
      </p>
    </blockquote>
    <v-row v-if="userAbout.birthday"  class="ml-1 mt-3 mb-2">
      <v-icon color="info" left> mdi-cake-variant </v-icon>
      <span class="pt-1" :title="userAbout.birthday">{{ userAbout.birthday }}</span>
    </v-row>
    <v-row v-if="userAbout.gender" class="ml-1">
      <v-icon color="info" left> {{userAbout.gender=="Masculino"?'mdi-face':'mdi-face-woman'}} </v-icon>
      <span :title="userAbout.gender" class="pt-1">{{ userAbout.gender }}</span>
    </v-row>
    
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  data: () => ({
    userAbout: {
      bio: "",
      birthday: "",
      gender: "",
    },
    apiDir: "user-about/",
  }),
  computed: {
    ...mapState(["baseUrl","authentication", "user"]),
  },
  mounted() {
    this.getUserAboutInfo();
    this.$root.$on("userInfoUpdated",()=>{
      this.getUserAboutInfo();
    });
  },
  methods: {
    getUserAboutInfo() {
      let username = this.$route.params.username;
      fetch(this.baseUrl + this.apiDir + "?username=" + username,{
       
      })
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.userAbout = response;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style>
.blockquote {
  font-size: 1.25rem;
  border-left: 0.5rem solid#478CCC;
  color: #6c757d;
  font-family: "Open Sans", "Segoe UI", "Roboto";
  line-height: 1.5;
  margin: 0 auto;
  max-width: 96%;
  position: relative;
  width: 100%;
}
.blockquote:before {
  font-size: 6.875rem;
  color: #478ccc;
  content: "\201C";
  font-family: "Noto Serif", "Georgia", "Karla", serif;
  font-size: 5.5rem;
  height: 3.75rem;
  left: 0.3rem;
  line-height: 1;
  max-width: 3.75rem;
  position: absolute;
  text-align: inherit;
  top: 0.1rem;
  width: 100%;
}
.blockquote:after {
  content: "";
}
</style>