<template>
  <div>
    <v-bottom-navigation grow id="bottom-nav" class="pt-1" color="primary">
      <v-row class="px-3 pt-0">
        <v-col class="pa-0">
          <v-btn icon class="pa-2" block exact :to="{ name: 'Home' }">
            <v-icon>mdi-home</v-icon>
          </v-btn>
        </v-col>
        <v-col class="pa-0">
          <v-btn icon class="pa-2" block exact :to="{ name: 'Explore' }">
            <v-icon>mdi-magnify</v-icon>
          </v-btn></v-col
        >
        <v-col class="pa-0">
          <v-btn icon class="pa-2" block exact :to="{ name: 'Notifications' }">
            <v-icon>mdi-bell</v-icon>
          </v-btn></v-col
        >
        <v-col class="pa-0">
          <v-btn icon class="pa-2" block exact :to="{ name: 'Inbox' }">
            <v-icon>mdi-comment-text</v-icon>
          </v-btn></v-col
        >
      </v-row>
    </v-bottom-navigation>
  </div>
</template>

<script>
export default {
  name: "FooterNav",
};
</script>

<style>
@media (max-width: 1264px) {
  #bottom-nav {
    display: block;
    position: fixed;
    bottom: -8px;
    z-index: 100;
    max-width: 100%;
    -webkit-box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.3);
    -moz-box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.3);
    box-shadow: 0px 0px 5px 1px rgba(0, 0, 0, 0.3);
  }
}
@media (min-width: 1264px) {
  #bottom-nav {
    display: none;
  }
}
</style>