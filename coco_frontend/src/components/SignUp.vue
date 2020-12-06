<template>
  <div>
    <v-dialog v-model="signUpDialog" max-width="600">
      <v-card>
        Reg[istrate] sesión con
        <v-row>
          <v-btn> Google </v-btn>
        </v-row>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapMutations, mapState } from "vuex";

export default {
  name: "SignUp",
  data: () => ({
    signUpDialog: false,
  }),
  created() {
    this.signUpDialog = this.forms.signUpDialog;
  },
  beforeUpdate() {
    let formDialog = {
      loginDialog: false,
      signUpDialog: this.signUpDialog,
    };
    this.updateFormsInfo(formDialog);
  },
  computed: {
    ...mapState(["forms"]),
  },
  methods: {
    ...mapMutations(["updateFormsInfo"]),
  },
};
</script>