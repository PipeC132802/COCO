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
        :color="user.profilePicture ? 'white' : 'secondary'"
        size="150"
        class="profile-picture"
      >
        <img v-if="user.profilePicture" :src="user.profilePicture" />
        <span v-else>{{ user.name.slice(0, 1) }}</span>
      </v-avatar>
      <h2 class="mb-2" :title="user.name">
        {{ user.name }}
        <span :title="'@' + user.username" class="text"
          >(@{{ user.username }})</span
        >
      </h2>
    </v-card-title>
    <v-card-text>
      <v-row justify="center">
        <span class="skills">
          <v-icon class="pb-1" left color="warning">
            mdi-head-lightbulb
          </v-icon>
          {{ user.skills }}
        </span>
      </v-row>
    </v-card-text>
    <v-divider>
     
    </v-divider>
       <v-card-actions>
            <v-btn>
                asd
            </v-btn>
        </v-card-actions>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "UserCover",
  data: () => ({
    apiDir: "account/",
    cover: "",
    user: {
      name: "",
      profilePicture: "",
      username: "",
      skills: "",
    },
  }),
  computed: {
    ...mapState(["baseUrl", "pixaKey"]),
  },
  created() {
    this.user.username = this.$route.params.username;
    this.getUserCoverInfo();
  },
  methods: {
    getUserCoverInfo() {
      fetch(this.baseUrl + this.apiDir + "?username=" + this.user.username)
        .then((response) => {
          return response.json();
        })
        .then((response) => {
          this.user.name = response.name;
          this.user.profilePicture = response.profile_picture;
          this.user.skills = response.skills.join(", ");
          document.title = this.user.name + `   (@${this.user.username}) / COCO`;
          this.searchCover();
        })
        .catch((err) => {
          console.error(err);
        });
    },
    searchCover() {
      let key = "key=" + this.pixaKey;
      let list = this.user.skills.split(",");
      let q =
        "q=" + list[Math.floor(Math.random() * list.length)];
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
          let img_slected = hits[Math.floor(Math.random() * hits.length)    ];
          this.cover = img_slected.largeImageURL;
        });
    },
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
</style>