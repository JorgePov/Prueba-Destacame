<template>
  <b-modal centered
           id="edit-employe"
           hide-footer>
    <template #modal-title>
      Editar empleado
    </template>
    <div class="d-block text-center">
      <form action="">
        <div class="mt-3 mb-2 label__select" v-if="!employeData.id">
            Email:
            <b-form-input placeholder="Email"
                      v-model="employeData.email"></b-form-input>
          </div>
          
          <div class="mt-3 mb-2 label__select" v-if="!employeData.id">
            Contraseña:
            <b-form-input placeholder="Contraseña"
                      v-model="employeData.password"></b-form-input>
          </div>
        <div class="mt-3 mb-2 label__select" >
            Nombres:
          </div>
        <b-form-input placeholder="Nombres"
                      v-model="employeData.first_name"></b-form-input>
        <div class="mt-3 mb-2 label__select" >
            Apellidos:
          </div>
        <b-form-input class="mt-2"
                      placeholder="Apellidos"
                      v-model="employeData.last_name"></b-form-input>
        <div class="mt-3 mb-2 label__select" v-if="!employeData.id">
            Identificación:
        <b-form-input class="mt-2 mb-2"
                      placeholder="Identificación"
                      v-model="employeData.id_card"></b-form-input>
          </div>
        <div class="mt-3 mb-2 label__select" >
            Edad:
          </div>
        <b-form-input class="mt-2"
                      type="number"
                      placeholder="Edad"
                      v-model="employeData.age"></b-form-input>
        <div class="d-flex align-items-center justify-content-end toogle">
          <span>Vendedor: </span>
          <label class="switch">
            <input v-model="employeData.is_seller"
                   @click="employeData.is_staff = false, employeData.is_driver = false"
                   type="checkbox">
            <span class="slider round"></span>
          </label>
        </div>
        <div class="d-flex align-items-center justify-content-end toogle">
          <span>Conductor: </span>
          <label class="switch">
            <input v-model="employeData.is_driver"
                   @click="employeData.is_staff = false, employeData.is_seller = false"
                   type="checkbox">
            <span class="slider round"></span>
          </label>
        </div>
        <div class="d-flex align-items-center justify-content-end toogle">
          <span>Administrador: </span>
          <label class="switch">
            <input v-model="employeData.is_staff"
                   @click="employeData.is_seller = false, employeData.is_driver = false"
                   type="checkbox">
            <span class="slider round"></span>
          </label>
        </div>
      </form>
    </div>
    <b-button
      class="mt-3"
      block
      variant="primary"
      @click="updated"
      v-if="employeData.id"
      >Editar</b-button
    >
    <b-button class="mt-3" block variant="primary" @click="created" v-else
      >Crear</b-button
    >
    <b-button class="mt-3" block @click="hideModal">Cancelar</b-button>
  </b-modal>
</template>
<script>
export default {
  props: ['employe'],
  data() {
    return {
      employeData: {}
    }
  },
  methods: {
    assignValues({ first_name, last_name, id, age, is_seller, is_driver, is_staff }) {
      this.employeData = {
        age,
        first_name,
        id,
        last_name,
        is_seller,
        is_driver,
        is_staff
      }
    },
    updated() {
      this.$axios
        .patch(`/api/v1/users/${this.employeData.id}`, this.employeData)
        .then((res) => {
          this.$emit("refresh-data");
          this.hideModal();
        })
        .catch(({ response }) => {
          if (response) {
            this.$store.commit("alert/setAlert", {
              variant: "danger",
              text: response.data.res,
              seconds: 3,
            });
          }
        });
    },
    created() {
      if (
        this.employeData.email != null &&
        this.employeData.password != null &&
        this.employeData.first_name != null &&
        this.employeData.last_name != null &&
        this.employeData.age != null &&
        this.employeData.id_card != null 
      ) {
        this.$axios
          .post(`/api/v1/users/signup`, this.employeData)
          .then((res) => {
            this.$emit("refresh-data");
            this.hideModal();
          })
          .catch(({ response }) => {
            if (response) {
              this.$store.commit("alert/setAlert", {
                variant: "danger",
                text: response.data.res,
                seconds: 3,
              });
            }
          });
      } else {
        this.$store.commit("alert/setAlert", {
          variant: "danger",
          text: "Debes llenar el formulario",
          seconds: 3,
        });
      }
    },
    hideModal() {
      this.$bvModal.hide("edit-employe");
    },
  },
  watch: {
    employe(value) {
      if (value.id) {
        this.assignValues(value)
        return
      }
      this.employeData = {
        is_staff: false,
        is_seller: false,
        is_driver: false
      }
    },
  }
}
</script>
<style lang="scss">
.toogle {
  margin-top: 10px;
  gap: 10px;
}
.label__select {
  text-align: start;
}
</style>