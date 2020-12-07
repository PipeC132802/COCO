import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

export default new Vuetify({
  theme: {
      options: {
        customProperties: true,
      },
    themes: {
      light: {
        primary: '#307ABD',
        secondary: '#09243D',
        accent: '#F06A24',
        error: '#BD4942',
        info: '#478CCC',
        success: '#09BD50',
        warning: '#F8A419'
      },
    },
  },
});


