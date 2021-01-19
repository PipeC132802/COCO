
  <template>
  <div>
    <div v-if="!loaded && field != 'detail'">
      <v-skeleton-loader
        v-for="index in 10"
        :key="index"
        type="list-item-avatar-two-line, article"
      ></v-skeleton-loader>
    </div>
    <div v-else-if="!loaded && (field == 'detail' || field == 'search')">
      <v-skeleton-loader
        type="list-item-avatar-two-line, article"
      ></v-skeleton-loader>
    </div>
    <div class="ml-3 mt-2" v-if="!barters.length">
      <p v-if="field == 'profile'">
        <span v-if="$route.params.username !== user.username">
          @{{ $route.params.username }} aún no ha publicado ningún trueque 🙄
        </span>
        <span v-else> No has publicado ningún trueque 🙄 </span>
      </p>
      <p v-else-if="field == 'reactions'">
        <span v-if="$route.params.username !== user.username">
          @{{ $route.params.username }} no ha reaccionado a ningún trueque 😒
        </span>
        <span v-else> No has reaccionado a ningún trueque 😒 </span>
      </p>
      <p v-else-if="field == 'recommendations'">
        No hemos encontrado sugerencias para ti 😔
      </p>
      <p v-else-if="field == 'newsfeed'">
        Nada en tu feed. ¡Date una vuelta y comparte con las personas de la
        comunidad! 🤗
      </p>
    </div>
    <v-card
      elevation="3"
      class="mb-4"
      v-for="barter in barters"
      :key="barter.id"
    >
      <v-list class="pb-0 mb-0" subheader two-line>
        <v-list-item class="pb-0 mb-0">
          <v-list-item-avatar color="secondary">
            <v-img
              v-if="barter.user.profile_picture"
              :src="barter.user.profile_picture"
            ></v-img>
            <span class="white--text" v-else>{{
              barter.user.name.slice(0, 1).toUpperCase()
            }}</span>
          </v-list-item-avatar>
          <v-list-item-content class="mt-0" style="line-heigth: 1">
            <v-list-item-title :title="barter.user.name">
              <span class="link"
                ><router-link
                  class="title--text"
                  :to="{
                    name: 'Profile',
                    params: { username: barter.user.username },
                  }"
                  >{{ barter.user.name }}</router-link
                ></span
              ><span class="grey--text ml-2" :title="'@' + barter.user.username"
                >@{{ barter.user.username }}</span
              >
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-icon class="mr-1" small>mdi-clock</v-icon>
              <small :title="timeSince(barter.created) | capitalize">{{
                timeSince(barter.created) | capitalize
              }}</small>
              
              <small v-if="barter.edited" class="ml-2">
                <v-chip title="Editado" small color="primary darken-5" label>
                  Editado
                </v-chip>
              </small>
              <small :title="barter.views +' vistas'" v-if="user.username == barter.user.username" class="ml-2">
                <v-chip small color="default" label>
                  <v-icon small left> mdi-eye </v-icon>
                  {{ barter.views }}
                </v-chip>
              </small>
            </v-list-item-subtitle>
          </v-list-item-content>
          <v-list-item-action>
            <v-menu
              top
              open-on-hover
              offset-y
              bottom
              transition="slide-y-transition"
            >
              <template v-slot:activator="{ on, attrs }">
                <v-btn dark icon v-bind="attrs" v-on="on">
                  <v-icon color="grey darken-3">mdi-dots-vertical</v-icon>
                </v-btn>
              </template>
              <v-list v-if="barter.user.username == user.username" class="pa-0">
                <v-list-item
                  class="item-menu pl-1"
                  v-for="(item, i) in items.self"
                  :key="i"
                  @click="setEvent(item.title, barter)"
                >
                  <v-list-item-title>
                    <v-icon class="ml-1" left>{{ item.icon }}</v-icon>
                    {{ item.title }}</v-list-item-title
                  >
                </v-list-item>
              </v-list>
              <v-list v-else class="pa-0">
                <v-list-item
                  class="item-menu pl-1"
                  v-for="(item, i) in items.other"
                  :key="i"
                >
                  <v-list-item-title>
                    <v-icon class="ml-1" left>{{ item.icon }}</v-icon>
                    {{ item.title }}</v-list-item-title
                  >
                </v-list-item>
              </v-list>
            </v-menu>
          </v-list-item-action>
        </v-list-item>
        <v-card-title class="mt-0 pt-0 mb-1">
          <router-link
            class="title--text"
            :title="barter.title"
            :to="{
              name: 'Barter',
              params: {
                username: barter.user.username,
                slug: barter.slug,
                pk: barter.id,
              },
            }"
            >{{ barter.title }}</router-link
          >
        </v-card-title>
        <v-card-subtitle class="pa-0 pt-0 mx-4">
          <v-chip :title="'Enseñaré ' + barter.skill" color="primary darken-1">
            <v-icon class="pl-1" small pill left> mdi-teach </v-icon>
            {{ barter.skill }}
          </v-chip>
          <v-chip
            :title="'Quiero aprender ' + barter.interest"
            class="ml-3"
            color="accent darken-1"
          >
            <v-icon class="pl-1" small pill left> mdi-school </v-icon>
            {{ barter.interest }}
          </v-chip>
          <v-chip :title="'🌎' + barter.about.place" class="ml-3" label>
            <v-icon small left>mdi-map-marker</v-icon>
            {{ barter.about.place }}
          </v-chip>
        </v-card-subtitle>
        <v-card-text class="px-4 mt-3 mb-0 pb-0">
          <p class="mb-0">
            {{ barter.about.description }}
          </p>
        </v-card-text>
      </v-list>

      <Reactions
        :id="'barter_' + barter.id"
        :barterId="barter.id"
        class="mx-1 mt-3"
        v-on:comments="showComments"
      />
      <BarterActions
        v-on:comments="showComments"
        :barterId="barter.id"
        class="mx-1 mt-0 ml-3"
      />
      <Comments
        v-if="barterComments == barter.id || field == 'detail'"
        :author="barter.user.username"
        class="mx-1 mt-0 ml-2"
        :barterId="barter.id"
      />
    </v-card>
    <v-dialog v-model="updateDialog" max-width="600px">
      <UpdateBarter
        v-if="updateDialog"
        v-on:barterUpdated="
          fetchBarterList();
          updateDialog = false;
        "
        :barter="barter2Edit"
      />
    </v-dialog>
  </div>
</template>

  <script>
import { mapState } from "vuex";
import moment from "moment";
import Reactions from "../components/Reactions.vue";
import BarterActions from "../components/BarterActions.vue";
import Comments from "../components/Comments.vue";
import UpdateBarter from "../components/UpdateBarter.vue";
export default {
  name: "BarterList",
  props: ["field", "pk"],
  components: {
    Reactions,
    BarterActions,
    Comments,
    UpdateBarter,
  },
  data: () => ({
    items: {
      self: [
        { title: "Editar", icon: "mdi-pencil" },
        { title: "Eliminar", icon: "mdi-delete" },
      ],
      other: [{ title: "Reportar", icon: "mdi-alert" }],
    },
    apiDir: {
      barter: "barter/",
      barterList: "barter-list/",
    },
    barters: [],
    loaded: false,
    barterComments: null,
    barter2Edit: "",
    barter2Delete: "",
    updateDialog: false,
  }),
  computed: {
    ...mapState(["baseUrl", "user", "authentication"]),
  },
  beforeMount() {
    this.$root.$on("comments", (data) => {
      if (data.barter === this.barterId) {
        this.getReactions();
      }
    });
    this.fetchBarterList();
  },
  methods: {
    fetchBarterList() {
      let query = "";
      if (this.field == "detail" || this.field == 'search') {
        query = `?id=${this.getPk()}&field=${
          this.field
        }&username=${this.getUsername()}&user_request=${this.user.id}`;
      } else {
        query = `?username=${this.getUsername()}&field=${
          this.field
        }&user=${this.getUsername()}&user_request=${this.user.id}`;
      }
      fetch(this.baseUrl + this.apiDir.barterList + query)
        .then((response) => response.json())
        .then((response) => {
          this.barters = response;
          this.loaded = true;
        })
        .catch((err) => console.error(err));
    },
    getUsername() {
      let username = "";
      username = this.$route.params.username;
      if (username == undefined) {
        username = this.user.username;
      }
      
      return username;
    },
    getPk() {
      return this.$route.params.pk | this.pk;
    },
    timeSince(date) {
      let timeSince = moment(date).locale("es").fromNow();
      return timeSince;
    },
    showComments(barter) {
      if (barter == this.barterComments) this.barterComments = null;
      else {
        this.barterComments = barter;
      }
    },
    setEvent(title, barter) {
      if (title == "Editar") {
        this.barter2Edit = barter;
        this.updateDialog = true;
      } else if (title == "Eliminar") {
        this.deleteBarter(barter);
      }
    },
    deleteBarter(barter) {
      fetch(this.baseUrl + this.apiDir.barter + `?barter=${barter.id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Token ${this.authentication.accessToken}`,
        },
      })
        .then((response) => response.json())
        .then(() => {
          this.fetchBarterList();
        })
        .catch((err) => console.error(err));
    },
    toProfile(username) {
      this.$router.push({ name: "Profile", params: { username: username } });
    },
  },
};
</script>

  <style  scoped>
.item-menu:hover {
  background: rgb(219, 219, 219);
  cursor: pointer;
}
p {
  font-size: 14pt;
  color: rgb(59, 59, 59);
}
.edit-tag {
  background: rgb(73, 73, 73);
  color: white;
  padding: 5px;
  letter-spacing: 0.5px;
  border-radius: 10%;
}
.link:hover {
  text-decoration: underline;
  cursor: pointer;
}
a {
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
</style>

