<template>
  <div>
    <v-card flat min-width="100" min-height="100vh">
      <v-container>
        <v-row align="center" justify="center">
          <v-card-title class="text-center">
            <v-avatar class="mr-3">
              <v-img src="@/assets/logo.png"></v-img>
            </v-avatar>
            <div class="text-center msg-verify">
              {{ message }}
            </div>
            <br />
          </v-card-title>
          <v-card-text class="text-center">
            
              <div v-if="!error && !loading" class="text-center msg-verify">
                En {{ time }} segundos serás redirigid@ para que inicies sesión.
              </div>
              <v-row align="center" justify="center">
              <div v-if="error" class="text-center msg-verify">
                <v-icon  v-if="error" left color="error"
                  >mdi-alert-circle</v-icon
                >
                Intenta de nuevo más tarde
              </div>
            </v-row>
            <v-progress-circular
              v-if="loading"
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-card-text>
        </v-row>
      </v-container>
    </v-card>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "Temp",
  data: () => ({
    loading: true,
    apiDir: "confirm-user/",
    message: "Verificando...",
    error: false,
    time: 10,
  }),
  computed: {
    ...mapState(["baseUrl"]),
  },
  mounted() {
    this.verifyEmail();
  },
  methods: {
    sleep(ms) {
      return new Promise((resolve) => setTimeout(resolve, ms));
    },
    verifyEmail() {
      fetch(this.baseUrl + this.apiDir + `?token=${this.$route.query.token}`, {
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.status == 200) {
            this.message = `Correo verificado exitosamente`;
            setInterval(() => {
              this.time -= 1;
            }, 1000);
            this.sleep(this.time * 1000).then(() => {
              location.href = "/";
            });
          } else {
            throw new Error();
          }
        })
        .catch((err) => {
          this.error = true;
          this.message = "Error";
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
};
</script>


<style scoped>
.msg-verify {
  color: rgb(65, 65, 65);
  font-size: calc(0.8vw + 1em);
}
</style>