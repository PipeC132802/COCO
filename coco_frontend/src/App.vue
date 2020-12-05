<template>
  <v-app>
    <v-card color="primary" height="100%">
    <LeftAside />
<v-main>
      <v-container class="content" fluid>
        
      </v-container>
    </v-main>
    
  </v-card>
      
  </v-app>
</template>

<script>
import LeftAside from '@/components/LeftAside';

export default {
  name: 'App',

  components: {
    LeftAside,
  },

  data: () => ({
    
  }),
};
</script>

<style scoped>
  .main{
    background: white;
    width: 100%;
    height: 100%;
  }
  .content{
    background: white;
    padding: 20px;
    min-height: 100vh;
    width: 100%;
  }
  .collapsible-aside{
    border: none;
    padding: 0px;
    background: orange;
  }
</style>
