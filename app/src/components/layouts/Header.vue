<template>
  <header class="header">
    <div class="d-flex align-items-center">
      <b-button v-b-toggle.sidebar
                class="custom__button" v-if="rol == 'admin'">
        <b-icon class="custom__icon"
                icon="list"></b-icon>
      </b-button>
      <h3 class="m-0 mr-1">Destacame</h3>
      <h3 class="m-0 second-text">Test</h3>
    </div>
    <div>
      <b-avatar text=""></b-avatar>
      <span class="text-capitalize mr-3">
        {{ $store.getters.getUser.first_name }}

      </span>
      <b-button class="custom__button"
                @click="logout">
        <b-icon class="custom__icon"
                icon="box-arrow-right"></b-icon>
      </b-button>
    </div>
  </header>
</template>
<script>
export default {
  name: 'Header',
  data() {
    return{
      rol:localStorage.getItem('rol')

    }
  },
  methods: {
    logout(){
      this.$store.commit('logout');
      this.$store.commit("aux/reset")
      this.$store.commit("seller/reset")
      this.$router.push('/login')
    }
  }
}
</script>
<style lang="scss" scoped>
.custom__button {
  background-color: transparent;
  border: none;
}

.custom__button:hover {
  background-color: darken($color: #0070F0, $amount: 10) !important;
}

.custom__icon {
  font-size: 25px;
}

.header {
  background-color: #0070F0;
  padding: 10px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  color: white;
}
</style>
