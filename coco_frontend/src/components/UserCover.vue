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
      <v-hover v-slot="{ hover }">
        <v-avatar
          :color="userP.profilePicture ? 'white' : 'secondary'"
          size="150"
          class="profile-picture"
        >
          <img v-if="userP.profilePicture" :src="userP.profilePicture" />
          <span v-else>{{ userP.name.slice(0, 1) }}</span>
          <div class="upload-profile" v-if="user.username == $route.params.username">
            <v-file-input
              class="file-upload"
              accept="image/png, image/jpeg, image/bmp"
              @change="addProfilePicture"
            ></v-file-input>
            <div class="align-self-center">
              <v-icon class="mt-12 mx-auto" x-large v-if="hover">
                mdi-upload
              </v-icon>
            </div>
          </div>
        </v-avatar>
      </v-hover>
      <h2 class="mb-2" :title="userP.name">
        {{ userP.name }}
        <span :title="'@' + userP.username" class="text"
          >(@{{ userP.username }})</span
        >
        <span
          v-if="userP.username == user.username"
          @click="go2Edit"
          class="route ml-3"
          title="Editar información de la cuenta"
          >Editar</span
        >
      </h2>
    </v-card-title>
    <v-card-text>
      <v-row justify="center">
        <span class="skills">
          <v-icon class="pb-1" left color="info"> mdi-calendar </v-icon>
          Se unió en
          {{ dateJoined | capitalize }}
        </span>
      </v-row>
      <v-row class="mt-2" justify="center">
        <v-btn
          class="mr-3"
          active-class="primary"
          text
          :to="{ name: 'Followers', params: { username: userP.username } }"
        >
          <strong class="mr-2">{{ userP.followers }}</strong
          >Seguidores
        </v-btn>
        <v-btn
          class="ml-3"
          active-class="primary"
          text
          :to="{ name: 'Following', params: { username: userP.username } }"
        >
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
        <FollowButton
          :from="user.username"
          :to="userP.username"
          v-on:followObj="followInfo"
          :text="true"
          :target="$route.params.username == user.username ? 'self' : 'other'"
        />
      </v-card-actions>
    </v-card-text>
    <v-dialog width="450" persistent v-model="profileDialog">
      <v-card class="px-3">
        <v-card-title class="pl-3">Subir foto de perfil </v-card-title>
        <v-img class="mx-auto" :src="profilePicture.url" max-width="400">
        </v-img>
        <v-card-actions>
          <v-btn
            :loading="loadingProfileBtn"
            class="mt-2 ml-3 mb-5"
            color="primary darken-3"
            @click="uploadProfilePicture"
          >
            Subir
          </v-btn>
          <v-btn
            @click="profileDialog = false"
            outlined
            class="mt-2 ml-3 mb-5"
            color="error darken-3"
            :disabled="loadingProfileBtn"
          >
            Cancelar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import { mapState } from "vuex";
import moment from "moment";

import FollowButton from "@/components/FollowButton.vue";
export default {
  name: "UserCover",
  props: ["user2Follow"],
  components: {
    FollowButton,
  },
  data: () => ({
    apiDir: {
      profilePicture: "profile-picture-user/",
      account: "account/",
    },
    cover: "",
    profileDialog: false,
    loadingProfileBtn: false,
    profilePicture: {
      file: "",
      url: "",
    },
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
      coverPhoto: ''
    },
  }),
  computed: {
    ...mapState([
      "baseUrl",
      "pixaKey",
      "authentication",
      "user",
      "profileFollowStatus",
    ]),
    dateJoined: function () {
      return moment(this.userP.dateJoined)
        .locale("es")
        .format("MMMM D [de] YYYY");
    },
  },
  watch: {
    profileFollowStatus: function () {
      this.userP.followers = this.profileFollowStatus.followers;
      this.userP.following = this.profileFollowStatus.following;
    },
  },
  beforeUpdate() {},
  beforeMount() {
    this.userP.username = this.$route.params.username;
    this.getUserCoverInfo();
  },
  methods: {
    getUserCoverInfo() {
      fetch(
        this.baseUrl +
          this.apiDir.account +
          "?username=" +
          this.userP.username +
          `&username_request=${this.user.username}`
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
          this.userP.coverPhoto = response.cover_photo;
          document.title = this.userP.name + ` (@${this.userP.username}) | COCO`;
          if(!response.cover_photo) this.searchCover();
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
    followInfo(followObj) {
      this.userP.followers = followObj.followers;
      this.userP.following = followObj.following;
      this.userP.followThisUser = followObj.follow_this_user;
    },
    go2Edit() {
      this.$router.push({
        name: "Edit",
        params: { username: this.userP.username },
      });
    },
    addProfilePicture(img) {
      this.profilePicture.file = img;
      this.profilePicture.url = URL.createObjectURL(img);
      this.profileDialog = true;
    },
    uploadProfilePicture() {
      this.loadingProfileBtn = true;
      if (this.profilePicture.file) {
        const formData = new FormData();
        
        formData.append("profile_picture", this.profilePicture.file);
        let headers = {
          Authorization: `Token ${this.authentication.accessToken}`,
        };
        delete headers["Content-Type"];
        fetch(this.baseUrl + this.apiDir.profilePicture, {
          method: "PUT",
          headers: headers,
          body: formData,
        })
          .then((response) => response.json())
          .then((response) => {
            this.userP.profilePicture = response.profile_picture;
          })
          .catch((err)=>console.error(err))
          .finally(()=>{
            this.loadingProfileBtn = false;
            this.profileDialog = false;
            this.profilePicture.file = '';
            this.profilePicture.url = '';
          })
      }
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
.actions {
  position: absolute;
  right: 20px;
  bottom: 15%;
}
.route {
  color: #478ccc;
  font-size: 12pt;
  font-weight: 200;
}
.route:hover {
  text-decoration: underline;
  cursor: pointer;
}
.show-btns {
  color: rgba(255, 255, 255, 1) !important;
}
.upload-profile {
  position: absolute;
  width: 150px;
  height: 150px;
  border-radius: 50%;
}
.upload-profile:hover {
  background: rgba(255, 255, 255, 0.2);
}
.file-upload {
  opacity: 0;
  filter: alpha(opacity=0);
  position: absolute;
  top: 0px;
  left: -35px;
  min-width: 0px;
  min-height: 0px;
  cursor: pointer;
  border-radius: 50%;
  z-index: 100;
}
.v-input__icon--prepend {
  opacity: 0;
  filter: alpha(opacity=0);
  position: absolute;
  top: -30px;
  width: 200px;
  height: 200px;
  border-radius: 50%;
}
</style>