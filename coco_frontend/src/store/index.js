import Vue from 'vue'
import Vuex from 'vuex'
Vue.use(Vuex)
import { readCookie } from "@/js/cookiesfunctions.js";

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
    profileFollowStatus: {
      followers: '',
      following: '',
      followThisUser: false,
    },
    wsBase : '127.0.0.1:8000',
    notifications: [],
    chat: '',
    chats: [],
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
    updateUserRequireMoreInfo(state, require) {
      state.userRequireMoreInfo = require;
    },
    updateProfileFollowStatus(state, profileFollowStatus) {
      state.profileFollowStatus = profileFollowStatus;
    },
    addNotification(state, notification){
      state.notifications.unshift(notification)
    },
    removeNotification(state){
      state.notifications.pop()
    },
    setChat(state, chat){
      state.chat = chat;
    },
    setChats(state, chats){
      state.chats = chats;
    },
    msgReceivedInbox(state, index){
      let aux = state.chats[index]
      state.chats.splice(index,1)
      state.chats.unshift(aux)
    },
    
    
    
  },
  actions: {
    
  },
  modules: {
  },
  getters: {
    loggedIn(state) {
      return !!state.authentication.accessToken || readCookie("token")
    }
  }
})
