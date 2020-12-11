<template>
  <div>
      <h1>Perfil</h1>
  </div>
</template>

<script>
import {mapState} from "vuex";
export default {
  created(){
    document.title = this.user.name + `   (@${this.user.username}) / COCO`
  },
  computed:{
    ...mapState(["user"])
  }
}
</script>

<style>

</style>