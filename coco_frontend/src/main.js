import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false

router.beforeEach((to,from,next) => {
  if(to.matched.some(record =>record.meta.requiresLogin)){
    if(!store.getters.loggedIn){
      next({name: 'Welcome'})
    } else{
      next()
    }
  }else{
    next()
  }
})

Vue.filter('capitalize', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
