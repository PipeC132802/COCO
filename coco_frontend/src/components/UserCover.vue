<template>
  <v-card>
    <v-img
      lazy-src="https://cdn.pixabay.com/photo/2015/08/28/11/27/space-911785_1280.jpg"
      aspect-ratio="1.7"
      max-height="300"
      :src="cover"
    >
      <template v-slot:placeholder>
        <v-row class="fill-height ma-0" align="center" justify="center">
          <v-progress-circular
            indeterminate
            color="grey lighten-5"
          ></v-progress-circular>
        </v-row>
      </template>
    </v-img>

    <v-card-title class="pb-0">
      <v-avatar
        :color="userP.profilePicture ? 'white' : 'secondary'"
        size="150"
        class="profile-picture"
      >
        <img v-if="userP.profilePicture" :src="userP.profilePicture" />
        <span v-else>{{ userP.name.slice(0, 1) }}</span>
      </v-avatar>
      <h2 class="mb-2" :title="userP.name">
        {{ userP.name }}
        <span :title="'@' + userP.username" class="text"
          >(@{{ userP.username }})</span
        >
      </h2>
    </v-card-title>
    <v-card-text>
      <v-row justify="center">
        <span class="skills">
          <v-icon class="pb-1" left color="info"> mdi-calendar </v-icon>
          {{ userP.dateJoined }}
        </span>
      </v-row>
      <v-row class="mt-2" justify="center">
        <v-btn class="mr-3"  active-class="primary"  text :to="{name: 'Followers', params:{username: userP.username,}}">
          <strong class="mr-2">{{ userP.followers }}</strong
          >Seguidores
        </v-btn>
        <v-btn class="ml-3" active-class="primary"  text :to="{name: 'Following', params:{username: userP.username,}}" >
          <strong class="mr-2">{{ userP.following }}</strong
          >Seguidos
        </v-btn>
      </v-row>
      <v-card-actions v-if="userP.username != user.username" class="actions">
        <v-chip
          class="mr-5"
          v-if="userP.followYou"
          color="info darken-5"
          text-color="white"
          title="Te sigue"
        >
          <v-avatar left>
            <v-icon>mdi-account-circle</v-icon>
          </v-avatar>
          Te sigue
        </v-chip>
        <FollowButton :followThisUser="userP.followThisUser" :from="user.username" :to="userP.username" v-on:followObj="followInfo"
        :target="$route.params.username == user.username?'self':'other'" />
      </v-card-actions>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
import FollowButton from "@/components/FollowButton.vue"
export default {
  name: "UserCover",
  props: ["user2Follow"],
  components:{
    FollowButton,
  },
  data: () => ({
    apiDir: "account/",
    cover: "",
    userP: {
      name: "",
      profilePicture: "",
      username: "",
      skills: "",
      dateJoined: "",
      followers: "",
      following: "",
      followYou: false,
      followThisUser: true,
    },
  }),
  computed: {
    ...mapState(["baseUrl", "pixaKey", "authentication", "user","profileFollowStatus"]),
    
  },
  watch:{
    profileFollowStatus: function(){
      this.userP.followers = this.profileFollowStatus.followers;
      this.userP.following = this.profileFollowStatus.following;
    }
  },
  beforeUpdate(){
  },
  beforeMount() {
    this.userP.username = this.$route.params.username;
    this.getUserCoverInfo();
  },
  methods: {
    getUserCoverInfo() {
      fetch(
        this.baseUrl +
          this.apiDir +
          "?username=" +
          this.userP.username +
          `&username_request=${this.user.username}`,
        {}
      )
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.userP.name = response.name;
          this.userP.profilePicture = response.profile_picture;
          this.userP.skills = response.skills.join(", ");
          this.userP.dateJoined = response.date_joined;
          this.userP.followers = response.followers;
          this.userP.following = response.following;
          this.userP.followThisUser = response.follow_this_user;
          this.userP.followYou = response.follow_you;
          document.title =
            this.userP.name + `(@${this.userP.username}) / COCO`;
          this.searchCover();
        })
        .catch((err) => {
          console.error(err);
        });
    },
    searchCover() {
      let key = "key=" + this.pixaKey;
      let list = this.userP.skills.split(",");
      let q = "q=" + list[Math.floor(Math.random() * list.length)];
      let image_type = "image_type=photo";
      let orientation = "orientation=horizontal";
      let min_width = "min_width=1080";
      let url =
        "https://pixabay.com/api/?" +
        [key, q, image_type, orientation, min_width].join("&");
      fetch(url)
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          let hits = response.hits;
          let total = hits.length;
          let img_slected = hits[Math.floor(Math.random() * hits.length)];
          this.cover = img_slected.largeImageURL;
        });
    },
    followInfo(followObj){
      this.userP.followers = followObj.followers;
      this.userP.following = followObj.following;
      this.userP.followThisUser = followObj.follow_this_user;
    }
    
  },
};
</script>

<style>
.profile-picture {
  position: absolute;
  box-sizing: content-box;
  top: 190px;
  left: 44.5%;
  border-radius: 50%;
  border: 3px solid white;
  color: white;
  font-size: 40pt;
}
h2 {
  margin: 35px auto;
  color: #09243dde;
}
.text {
  font-size: 16pt;
  color: #747474;
}
.skills {
  font-size: 14pt;
}
.actions {
  position: absolute;
  right: 20px;
  bottom: 15%;
}
</style>