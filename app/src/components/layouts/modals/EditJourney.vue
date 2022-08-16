<template>
  <b-modal centered id="edit-journey" hide-footer>
    <template #modal-title> 
      <div v-if="journeyData.id">
        {{
          `${journeyData.id} - ${journeyData.origin} / ${journeyData.destination}`
        }}
      </div>
      <div v-else>Nuevo Trayecto</div>
      </template>
    <div class="edit-journey">
      <form action="">
        <b-form-input
          class="mt-2"
          type="text"
          v-model="journeyData.origin"
          placeholder="Origen"
          v-if="!journeyData.id"
        ></b-form-input>
        <b-form-input
          class="mt-2"
          type="text"
          v-model="journeyData.destination"
          placeholder="Destino"
          v-if="!journeyData.id"
        ></b-form-input>
        <b-form-input
          class="mt-2"
          type="number"
          v-model="journeyData.price"
          placeholder="Precio"
        ></b-form-input>
        <div v-if="journeyData.id"
             class="d-flex align-items-center justify-content-end toogle">
          <span>Activo: </span>
          <label class="switch">
            <input v-model="journeyData.is_active"
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
      v-if="journeyData.id"
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
  props: ["journey"],
  data() {
    return {
      journeyData:{}
    };
  },
  watch: {
    journey(value) {
      if (value.id) {
        this.assignValues(value);
        return;
      }
      this.journeyData = {
        destination:null,
        origin: null,
        price: null,
        is_active: false,
      };
    },
  },
  methods: {
    assignValues({ id, destination, origin, price, is_active }) {
      this.journeyData = {
        id,
        destination,
        origin,
        price,
        is_active,
      };
    },
    updated() {
      this.$axios
        .patch(`/api/v1/journeys/${this.journeyData.id}`, this.journeyData)
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
        this.journeyData.destination != null &&
        this.journeyData.origin != null &&
        this.journeyData.price != null 
      ) {
        delete this.journeyData.is_active;
        this.$axios
          .post(`/api/v1/journeys`, this.journeyData)
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
      this.$bvModal.hide("edit-journey");
    },
  },
};
</script>