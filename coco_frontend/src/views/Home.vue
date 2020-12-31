<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col sm="12" md="8" lg="9" xl="10">
          <NewBarter />
          <BarterList :field="'newsfeed'" />
        </v-col>
        <v-col>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
import NewBarter from "@/components/NewBarter";
import BarterList from "@/components/BarterList.vue";

export default {
  name: "Home",

  components: {
    NewBarter,
    BarterList
  },
  created(){
    document.title = "Inicio / COCO"
  }
};
</script>
