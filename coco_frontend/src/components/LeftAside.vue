<template>
  <div >
    <v-navigation-drawer
      permanent
      app
      color="primary"
      class="navigation pa-0 ma-0"
      dark
      expand-on-hover
    >
      <template v-slot:prepend class="ma-0">
        <v-list-item  class="pa-0 pl-2 ma-0" two-line>
          <v-list-item-avatar size="30" color="secondary" class="mt-4 ml-1">
            <img  v-if="user.profile_picture" :alt="'perfil de ' + user.name" :src="user.profile_picture" />
            <span v-else>{{user.name.slice(0,1).toUpperCase()}}</span>
          </v-list-item-avatar>
          <v-list-item-content class="white--text">
            <v-list-item-title :title="user.name">{{user.name}}</v-list-item-title>
            <v-list-item-subtitle :title="'@'+user.username" class="secondary--text">@{{user.username}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </template>
        <v-divider dark></v-divider>
        
      <v-list dense >
          
        <v-list-item  class="item" :title="item.title" active-class="white primary--text"  :to="{ name: item.link }" exact  v-for="item in items" :key="item.title" link>
          <v-list-item-icon>
              <v-badge
          :content="item.value"
          :value="item.value"
          color="accent"
          overlap
        >
          <v-icon>{{ item.icon }}</v-icon>
        </v-badge>
            
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script>
import {mapState, mapMutations} from "vuex";
export default {
  name: "LeftAside",
  data: () => ({
    user: {
      profile_picture: '',
      name: "",
      username: "",
    },
      apiDir: 'user-status/',
    drawer: true,
        items: [
          { title: 'Inicio', icon: 'mdi-home',  link: 'Home', value:'' },
          { title: 'Explorar', icon: 'mdi-magnify', link: 'Explore',  value:'' },
          { title: 'Notificaciones', icon: 'mdi-bell', link: 'Notifications',  value:'' },
          { title: 'Mensajes', icon: 'mdi-message-text', link: 'Inbox',  value:'' },
          { title: 'Perfil', icon: 'mdi-account', link: 'Profile',  value:'' },
          { title: 'Ajustes ', icon: 'mdi-cogs', link: 'Settings',  value:'' },
        ],
        mini: true,
  }),
  computed:{
      ...mapState(["baseUrl"])
  },
  created(){
      console.log(this.apiDir)
      fetch(this.baseUrl + this.apiDir,{
          method: 'GET',
          headers:  {
              'Authorization': 'Token 604fc20916f801861500ad268ab3e93b4f4c2433'
          }
      })
      .then((respose)=>{
         return respose.json()
      })
      .then((respose)=>{
           this.user = respose;
           this.items[2].value = respose.unread_notifications;
           this.items[3].value = respose.unread_messages;
           this.setUser(respose);
      })

  },
  methods:{
      ...mapMutations(["setUser"]),
  }
};
</script>
<style scoped>
    .navigation{
        color: white;
        border-radius: 0 10px 0px 0;
    }
    .item{
        border-radius: 15px;
        height: 50px;
        padding-top: 5px ;
    }
    
</style>