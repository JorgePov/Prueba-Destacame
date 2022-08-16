<template>
  <b-alert :show="dismissCount"
           dismissible
           class="alert"
           :variant="variant"
           @dismissed="dismissCount = 0"
           @dismiss-count-down="countDownChanged">
    {{ text }}
  </b-alert>
</template>

<script>
export default {
  name: 'Alert',
  data() {
    return {
      dismissCount: 0
    }
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCount = dismissCountDown
      if (dismissCountDown === 0) {
        this.$store.commit('alert/reset')
      }
    }
  },
  computed: {
    variant() {
      return this.$store.getters['alert/getVariant']
    },
    text() {
      return this.$store.getters['alert/getText']
    },
    count() {
      return this.$store.getters['alert/getCount']
    }
  },
  watch: {
    count: function (value) {
      this.dismissCount = value
    }
  }
}
</script>
<style>
.alert {
  position: fixed !important;
  bottom: 10px;
  right: 10px;
}
</style>