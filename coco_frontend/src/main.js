import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify';
import GAuth from 'vue-google-oauth2'

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

const gauthOption = {
  clientId: '264267313754-eqh81o57fmgmuv9i90v60s9t6bt6mek4.apps.googleusercontent.com',
  scope: 'email',
  prompt: 'consent',
  fetch_basic_profile: true
}

Vue.use(GAuth, gauthOption)
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
