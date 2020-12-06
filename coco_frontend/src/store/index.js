import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user:'',
    baseUrl: 'http://127.0.0.1:8000/coco/api/v1.0/',
  },
  mutations: {
    setUser(state,user){
      state.user = user;
    }
  },
  actions: {
  },
  modules: {
  }
})
