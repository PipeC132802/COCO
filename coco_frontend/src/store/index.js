import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    authentication: {
      accessToken: null,
      userIsAuthenticated: false,
    },
    forms: {
      loginDialog: false,
      signUpDialog: false,
    },
    user: '',
    baseUrl: 'http://127.0.0.1:8000/coco/api/v1.0/',
    userRequireMoreInfo: true,
    pixaKey: '19499640-f691e6b92721afc93a5b52556',
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    updateAuthInfo(state, authObj) {
      state.authentication = authObj;
    },
    updateFormsInfo(state, formDialogs) {
      state.forms = formDialogs;
    },
    updateUserRequireMoreInfo(state, require){
      state.userRequireMoreInfo = require;
    }
   
    
  },
  actions: {


  },
  modules: {
  },
  getters: {
    loggedIn(state) {
      return state.authentication.accessToken != null
    }
  }
})
