<template>
  <div>
    <v-bottom-navigation grow id="bottom-nav" class="pt-3" color="primary">
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
            <v-icon>mdi-message</v-icon>
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
    bottom: 0%;
    z-index: 100;
    max-width: 100%;
  }
}
@media (min-width: 1264px) {
  #bottom-nav {
    display: none;
  }
}
</style>