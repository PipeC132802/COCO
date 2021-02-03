    <template>
  <div>
    <v-menu
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      transition="scale-transition"
      offset-y
      min-width="290px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          v-model="birthday"
          label="Cumpleaños"
          prepend-icon="mdi-calendar"
          readonly
          v-bind="attrs"
          v-on="on"
        ></v-text-field>
      </template>
      <v-date-picker
        ref="picker"
        v-model="birthday"
        :max="new Date().toISOString().substr(0, 10)"
        min="1950-01-01"
        @change="save"
      ></v-date-picker>
    </v-menu>
    <v-select
    v-model="gender"
          :items="items"
          label="Género"
        ></v-select>
  </div>
</template>

    <script>
export default {
    name: 'Personal',
  data: () => ({
    birthday: null,
    gender: null,
    menu: false,
    items: ['Femenino', 'Masculino', 'Prefiero no decirlo']
  }),
  beforeUpdate(){
      let aboutObj = {
        birthday: this.birthday,
        gender: this.gender,
      };
     
      this.$emit("about", aboutObj);
  },
  watch: {
    menu(val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = "YEAR"));
    },
  },
  methods: {
    save(date) {
      this.$refs.menu.save(date);
    },
  },
};
</script>

    <style>
</style>