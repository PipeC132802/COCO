<template>
  <v-container class="ma-0 pt-0">
      <CommentForm :barterId="barterId" />
      Comments {{barterId}}
  </v-container>
</template>

<script>
import CommentForm from "../components/CommentForm.vue"
export default {
    name: 'Comments',
    props: ['barterId'],
    components:{
        CommentForm
    }
}
</script>

<style>

</style>