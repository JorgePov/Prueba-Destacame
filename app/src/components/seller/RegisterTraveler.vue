<template>
  <b-card no-body
          class="card__travel w-100">
    <b-card-body class="text-center">
      <b-card-title>Registrar pasajero</b-card-title>
      <form>
        <label class="label__form m-0">Cedula</label>
        <b-form-input type="number"
                      class="w-100"
                      placeholder="Cedula"
                      v-model="data.id_card"></b-form-input>
        <label class="label__form m-0 mt-2">Nombre</label>
        <b-form-input type="text"
                      class="w-100"
                      placeholder="Nombre"
                      v-model="data.first_name"></b-form-input>
        <label class="label__form m-0 mt-2">Apellido</label>
        <b-form-input type="text"
                      class="w-100"
                      placeholder="Apellido"
                      v-model="data.last_name"></b-form-input>
        <label class="label__form m-0 mt-2">Edad</label>
        <b-form-input type="number"
                      class="w-100"
                      placeholder="Edad"
                      v-model="data.age"></b-form-input>
      </form>
      <b-button class="mt-2 mb-0 search__button"
                variant="primary"
                @click="handleClick">Registrar</b-button>
    </b-card-body>
  </b-card>
</template>
<script>
export default {
  props: ['data'],
  data() {
    return {
      selected: null,
    }
  },
  methods: {
    handleClick(){
      this.$emit('traveler-register',this.data)
    }
  }
}


</script>
<style>
.label__form {
  font-weight: 500;
  float: left;
}
</style>
