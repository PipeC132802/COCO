import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    authentication: {
      accessToken: null,
      userIsAuthenticated: false,
    },
    forms:{
      loginDialog: false,
      signUpDialog: false,
    },
    user:'',
    baseUrl: 'http://127.0.0.1:8000/coco/api/v1.0/',
  },
  mutations: {
    setUser(state,user){
      state.user = user;
    },
    updateAuthInfo(state, tokenObj){
      state.authentication = tokenObj;
    },
    updateFormsInfo(state, formDialogs){
      state.forms = formDialogs;
    }
  },
  actions: {
    
  
  },
  modules: {
  },
  getters:{
    loggedIn(state){
      return state.authentication.accessToken != null
    }
  }
})
