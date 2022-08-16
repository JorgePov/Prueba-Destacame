<template>
  <div class="layout__container">
    <Header />
    <router-view></router-view>
    <Alert />
    <Footer />
  </div>
</template>
<style>
.layout__container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
<script>
import Header from "@/components/layouts/Guest/Header.vue";
import Footer from "@/components/layouts/Footer.vue";
import Alert from "@/components/layouts/Alert.vue";

export default {
  name: "dashboard-layout",
  components: {
    Header,
    Footer,
    Alert,
  },
};
</script>
