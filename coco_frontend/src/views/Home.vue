<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col sm="12" md="8" lg="9" xl="10">
          <NewBarter />
        </v-col>
        <v-col>
          asdads
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
import NewBarter from "@/components/NewBarter";
export default {
  name: "Home",

  components: {
    NewBarter,
  },
};
</script>
