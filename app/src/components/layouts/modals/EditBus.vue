<template>
  <b-modal centered
           id="edit-bus"
           hide-footer>
    <template #modal-title>
      {{ dataBus.id ? 'Editar Bus' : 'Crear Bus' }}
    </template>
    <div class="d-block text-center">
      <form action="">
        <div v-if="!dataBus.id">
          <span class="title">Placa:</span>
          <b-form-input placeholder="Placa"
                        v-model="dataBus.bus_plate"></b-form-input>
        </div>
        <div>
          <span class="title">Capacidad:</span>
          <b-form-input class="mt-2"
                        placeholder="Capacidad"
                        v-model="dataBus.capacity"></b-form-input>
        </div>

        <div v-if="dataBus.id"
             class="d-flex align-items-center justify-content-end toogle">
          <span>Activo: </span>
          <label class="switch">
            <input v-model="dataBus.is_active"
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
      v-if="dataBus.id"
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
  props: ['bus'],
  data() {
    return {
      dataBus: {}
    }
  },
  methods: {
    assignValues({ id,capacity, is_active, bus_plate }) {
      this.dataBus = {
        id,
        capacity,
        is_active,
        bus_plate
      }
    },
    updated() {
      this.$axios
        .patch(`/api/v1/buses/${this.dataBus.bus_plate}`, this.dataBus)
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
        this.dataBus.bus_plate != null
      ) {
        delete this.dataBus.is_active;
        this.$axios
          .post(`/api/v1/buses`, this.dataBus)
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
      this.$bvModal.hide("edit-bus");
    },
  },
  watch: {
    bus(value) {
      if (value.bus_plate) {
        this.assignValues(value)
        return
      }
      this.dataBus = {}
    }
  }
}
</script>
<style lang="scss">
.title {
  float: left;
}
</style>