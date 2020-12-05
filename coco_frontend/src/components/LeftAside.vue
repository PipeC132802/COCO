<template>
  <div >
    <v-navigation-drawer
      v-model="drawer"
      expand-on-hover
      app
      enable-resize-watcher
      clipped
      permanent
      color="primary"
      class="navigation"
      dark
    >
      <template v-slot:prepend>
        <v-list-item  class="pa-2 ma-0" two-line>
          <v-list-item-avatar>
            <img src="https://randomuser.me/api/portraits/women/81.jpg" />
          </v-list-item-avatar>

          <v-list-item-content class="white--text">
            <v-list-item-title>{{user.name}}</v-list-item-title>
            <v-list-item-subtitle class="secondary--text">@{{user.username}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </template>


      <v-list dense >
          
        <v-list-item  class="item" active-class="white primary--text"  :to="{ name: item.link }" exact  v-for="item in items" :key="item.title" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
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
export default {
  name: "LeftAside",
  data: () => ({
    user: {
      name: "Felipe Cerquera",
      username: "pipe",
    },
    drawer: true,
        items: [
          { title: 'Inicio', icon: 'mdi-home',  link: 'Home' },
          { title: 'Explorar', icon: 'mdi-magnify', link: 'Explore' },
          { title: 'Notificaciones', icon: 'mdi-bell', link: 'Notifications' },
          { title: 'Mensajes', icon: 'mdi-message-text', link: 'Inbox' },
          { title: 'Perfil', icon: 'mdi-account', link: 'Profile' },
          { title: 'Ajustes ', icon: 'mdi-cogs', link: 'Settings' },
        ],
        mini: true,
  }),
};
</script>
<style scoped>
    .navigation{
        color: white;
        border-radius: 10px;
    }
    .item{
        border-radius: 15px;
        height: 50px;
        padding-top: 5px ;
    }
    
</style>