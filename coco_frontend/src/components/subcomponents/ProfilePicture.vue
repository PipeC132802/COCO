<template>
  <div>
    <div class="img-preview">
      <v-icon v-if="!avatar" size="280"> mdi-account </v-icon>
      
<v-img v-else
  :src="avatar"
  size="280"></v-img>
      <v-avatar  size="280"> </v-avatar>
    </div>
    <v-file-input
      v-model="file"
      accept="image/png, image/jpeg, image/bmp"
      prepend-icon="mdi-camera"
      label="Foto de perfil"
      @change="profilePicture"
    ></v-file-input>
  </div>
</template>

<script>
export default {
  name: "ProfilePicture",
  data: () => ({
    file: null,
    avatar: "",
  }),
  beforeUpdate(){
    this.$emit("profilePicture", this.file);
  },
  methods: {
    profilePicture() {
      if (this.file) {
        this.avatar = URL.createObjectURL(this.file);
      } else {
        this.avatar = "";
      }
    },
  },
};
</script>

<style  scoped>
.img-preview {
  box-sizing: content-box;
  height: 280px;
  width: 280px;
  margin: 15px auto;
  background: rgb(236, 236, 236);
  border-radius: 50%;
  padding: 10px auto;
  overflow: hidden;
}
</style>
