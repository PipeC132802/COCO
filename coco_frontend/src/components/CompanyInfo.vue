<template>
  <div class="mt-5">
    <v-container content="center">
      <span class="mr-1"
        ><router-link class="link title--text" :to="{ name: 'AboutUs' }"
          >Sobre COCO</router-link
        ></span
      >
      • <span class="link mr-1">Ayuda</span> •
      <span class="link mr-1">Términos y condiciones</span> •
      <span class="primary--text link" @click="sheet = !sheet">Más</span>
    </v-container>

    <v-row class="pl-5 mb-1" align="center">
      <v-img
        class="mr-2"
        src="@/assets/logo.png"
        max-height="23"
        max-width="23"
      >
      </v-img>
      <span class="primary--text mr-2 COCO"> COCO </span>
      <span
        ><small class="pt-2">
          Todos los derechos reservados © {{ currentYear }}
        </small></span
      >
    </v-row>

    <v-bottom-sheet v-model="sheet">
      <v-sheet height="200px">
        <v-container class="pb-0">
          <v-row class="mt-2">
            <v-img
              class="mr-2 ml-2"
              src="@/assets/logo.png"
              max-height="35"
              max-width="35"
            >
            </v-img>
            <span class="primary--text mr-2 COCO"> COCO </span>
          </v-row>
          <v-row class="mt-0">
            <v-col class="pt-0">
              <v-row class="mb-1" align="center">
                <v-col sm="12" class="mt-2pt-0 pb-0">
                  <router-link
                    class="link title--text"
                    :to="{ name: 'AboutUs' }"
                    >Sobre COCO</router-link
                  >
                </v-col>
                <v-col sm="12" class="pt-0 pb-0">
                  <router-link
                    class="link title--text"
                    :to="{ name: 'CommunityRules' }"
                    >Reglas comunitarias</router-link
                  >
                </v-col>
                <v-col sm="12" class="pt-0 pb-0">
                  <router-link
                    class="link title--text"
                    :to="{ name: 'AboutUs' }"
                    >Términos y condiciones</router-link
                  >
                </v-col>
                <small class="ml-3 mt-2 grey--text"
                  >Todos los derechos reservados © {{ currentYear }}</small
                >
              </v-row>
            </v-col>
            <v-col class="pt-0">
                <v-row class="mb-1" align="center">
                <v-col sm="12" class="mt-2pt-0 pb-0">
                    <v-icon>mdi-help-circle-outline</v-icon>
                  <router-link
                    class="link title--text"
                    :to="{ name: 'AboutUs' }"
                    >  Ayuda</router-link
                  >
                </v-col>              
              </v-row>
            </v-col>
            <v-col></v-col>
          </v-row>
        </v-container>
      </v-sheet>
    </v-bottom-sheet>
  </div>
</template>

<script>
export default {
  name: "CompanyInfo",
  data: () => ({
    sheet: false,
    currentYear: new Date().getFullYear(),
  }),
};
</script>

<style>
.COCO {
  font-size: 12pt;
  font-weight: bold;
  padding-top: 3px;
}
.link {
  text-decoration: none;
  font-size: 10pt;
}
</style>