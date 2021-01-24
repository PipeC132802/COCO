<template>
  <v-container fluid>
    <v-row justify="center" class="px-0">
      <v-col cols="12" sm="12" md="4">
        <InboxComponent />
      </v-col>
      <v-col class="chatlist" sm="12" md="8">
        <div v-if="chat">
          <router-view class="mt-2" />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import InboxComponent from "../components/Inbox.vue";
export default {
  components: {
    InboxComponent,
  },
  data: () => ({
    chat: null,
  }),
  created() {
    document.title = "Inbox | COCO";
  },
  mounted() {
    
  },
  methods: {
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
  },
};
</script>

<style>
.chatlist{
  border-left: 1px solid rgb(211, 211, 211);
}
</style>