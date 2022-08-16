<template>
  <div class="login__container">
    <form action="" class="login__form">
      <img src="../assets/img/unnamed.png" alt="" width="250px" />
      <h3>
        <span class="title">Destacame</span>
        Test
      </h3>

      <b-input-group class="mt-2">
        <b-input-group-prepend>
          <b-input-group-text>
            <b-icon icon="person-fill"></b-icon>
          </b-input-group-text>
        </b-input-group-prepend>
        <b-form-input
          :class="[isEmailValid()]"
          type="email"
          v-model="data.email"
        >
        </b-form-input>
      </b-input-group>
      <b-input-group class="mt-2">
        <b-input-group-prepend>
          <b-input-group-text>
            <b-icon icon="key-fill"></b-icon>
          </b-input-group-text>
        </b-input-group-prepend>
        <b-form-input type="password" v-model="data.password"> </b-form-input>
      </b-input-group>
      <b-button block class="mt-2 mb-0" variant="primary" @click="userLogin"
        >Ingresar</b-button
      >
      <div class="mt-2">
        <router-link to="/">Eres pasajero ?</router-link>
      </div>
    </form>
    <div class="mt-2">
      <p>*only dev*</p>
      <button @click="changedUser('admin')">Admin</button>
      <button @click="changedUser('driver01')">Driver</button>
      <button @click="changedUser('seller01')">Seller</button>
    </div>
    <Alert />
  </div>
</template>

<script>
import Alert from "@/components/layouts/Alert.vue";
export default {
  data() {
    return {
      data: {
        email: "admin@destacame.com",
        password: "dddd",
      },
      pathlogin: "",
      reg: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,24}))$/,
    };
  },
  components: {
    Alert,
  },
  created() {
    this.$store.commit("logout");
  },
  computed: {
    user() {
      return this.$store.getters["getUser"];
    },
  },
  methods: {
    changedUser(user) {
      this.data.email = `${user}@destacame.com`;
    },
    isEmailValid() {
      return this.data.email == ""
        ? ""
        : !this.reg.test(this.data.email) && "has-error";
    },
    userLogin() {
      this.$axios
        .post("/api/v1/users/login", this.data)
        .then(({ data }) => {
          this.$store.commit("setToken", data.access);
          let action = async () => {
            await this.$store.dispatch("setCurrentUser");
            this.$store.commit("setRol");
            this.pathlogin = this.redirectRol();
          };
          action();
        })
        .catch((err) => {
          this.$store.commit("alert/setAlert", {
            variant: "danger",
            text: "Error en credenciales",
            seconds: 3,
          });
        });
    },
    redirectRol() {
      let path = { driver: "/driver", seller: "/seller" , admin:"/admin"}
      this.$router.push(path[this.$store.getters.getRol]) ;
    },
  },
};
</script>

<style lang="scss" scoped>
.login__container {
  width: 100vw;
  height: 100vh;
  display: grid;
  place-items: center;
  background-color: #c0c0c0;
}

.has-success {
  border: 1px solid #67b168;
}

.has-error {
  border: 1px solid red;
}

.login__form {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background-color: #e2e2e2;
  border-radius: 10px;
  text-align: center;
  font-weight: 500;
  height: 500px;
  width: 100%;
  max-width: 400px;

  .title {
    text-align: center;
    color: #0070f0;
  }
}
</style>

