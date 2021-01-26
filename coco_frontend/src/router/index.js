import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
  
  {
    path: '/',
    name: 'Welcome',
    component: () => import('../views/Welcome.vue')
  },
  {
    path: '/page-not-found',
    name: 'NotFound',
    component: () => import('../views/error/NotFound.vue')
  },
  {
    path: '/about',
    name: 'AboutUs',
    component: () => import('../views/AboutCOCO.vue')
  },
  {
    path: '/community-rules',
    name: 'CommunityRules',
    component: () => import('../views/AboutCOCO.vue')
  },
  {
    path: '/user/complete-info',
    name: 'MoreInfo',
    component: () => import('../views/MoreUserInfo.vue'),
    meta: {
      requiresLogin: true
    }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: {
      requiresLogin: true
    }
  },
  {
    path: '/search',
    name: 'Explore',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Explore.vue'),

  },
  {
    path: '/notifications',
    name: 'Notifications',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Notifications.vue'),
    meta: {
      requiresLogin: true
    }
  },
  {
    path: '/inbox',
    name: 'Inbox',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Inbox.vue'),
    meta: {
      requiresLogin: true
    },
    children: [
      { path: 'messages/:id', name: 'Messages', component: () => import('../views/subviews/Messages.vue') },
    ]
  },
  {
    path: '/settings',
    name: 'Settings',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Settings.vue'),
    meta: {
      requiresLogin: true
    },
    children: [
      { path: 'account', name: 'Account', component: () => import('../views/subviews/Account.vue') },
      { path: 'account/your-info', name: 'YourInfo', component: () => import('../views/subviews/AccountInfo.vue') },
      { path: 'account/password', name: 'Password', component: () => import('../views/subviews/Password.vue') },
      { path: 'account/deactivate', name: 'Deactivate', component: () => import('../views/subviews/DeactivateAccount.vue') },
      { path: 'security', name: 'Security', component: () => import('../views/subviews/Security.vue') },
      { path: 'notifications', name: 'NotificationsSettings', component: () => import('../views/subviews/Notifications.vue') },
      { path: 'more', name: 'Resources', component: () => import('../views/subviews/More.vue') },
    ]
  },
  {
    path: '/:username',
    name: 'Profile',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Profile.vue'),
    children: [
      {
        path: 'followers', name: 'Followers', component: () => import('../views/subviews/Followers.vue')
      },
      { path: 'following', name: 'Following', component: () => import('../views/subviews/Following.vue') },
      { path: 'edit', name: 'Edit', component: () => import('../views/subviews/EditProfile.vue') },
    ]

  },
  {
    path: '/:username/barters/:slug/:pk',
    name: 'Barter',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import('../views/Barter.vue'),
  },
  

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
