<template>
  <b-modal centered id="edit-travels" hide-footer>
    <template #modal-title>
      <div v-if="travelData.id">
        {{
          `${travel.id} - ${travel.journey.origin} / ${travel.journey.destination}`
        }}
      </div>
      <div v-else>Nuevo Viaje</div>
    </template>
    <div class="d-block text-center">
      <form class="w-100 form__search p-2">
        <div class="input__group mt-2" v-if="!travelData.id">
          <b-form-select
            class="select__option"
            v-model="travelData.journey"
            :options="journeyOptions"
          >
            <template #first>
              <b-form-select-option :value="null" disabled
                >Trayectos</b-form-select-option
              >
            </template>
          </b-form-select>
        </div>
        <div class="input__group mt-2" v-if="!travelData.id">
          <b-form-select
            class="select__option"
            v-model="travelData.scheduled"
            :options="scheduledOptions"
          >
            <template #first>
              <b-form-select-option :value="null" disabled
                >Horarios</b-form-select-option
              >
            </template>
          </b-form-select>
        </div>
        <div class="input__group mt-2">
          <div class="mt-3 mb-2 label__select" v-if="travelData.id">Bus:</div>
          <b-form-select
            class="select__option"
            v-model="travelData.bus"
            :options="busesOptions"
          >
            <template #first>
              <b-form-select-option :value="null" disabled
                >Buses</b-form-select-option
              >
            </template>
          </b-form-select>
        </div>
        <div class="input__group mt-2">
          <div class="mt-3 mb-2 label__select" v-if="travelData.id">
            Conductor:
          </div>
          <b-form-select
            class="select__option"
            v-model="travelData.driver"
            :options="driversOptions"
          >
            <template #first>
              <b-form-select-option :value="null" disabled
                >Conductor</b-form-select-option
              >
            </template>
          </b-form-select>
        </div>
        <div v-if="travelData.id"
             class="d-flex align-items-center justify-content-end toogle">
          <span>Activo: </span>
          <label class="switch">
            <input v-model="travelData.is_active"
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
      v-if="travelData.id"
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
  props: ["travel"],
  data() {
    return {
      travelData: {},
      driversOptions: [],
      busesOptions: [],
      journeyOptions: [],
      scheduledOptions: [],
      buses: [],
      drivers: [],
      journey: [],
      scheduled: [],
    };
  },
  watch: {
    travel(value) {
      if (value.id) {
        this.assignValues(value);
        return;
      }
      this.travelData = {
        journey: null,
        scheduled: null,
        bus: null,
        driver: null,
        is_active: false,
      };
    },
  },
  async mounted() {
    let { data: buses } = await this.$axios.get(`/api/v1/buses`);
    this.buses = buses;
    let { data: drivers } = await this.$axios.get(`/api/v1/drivers`);
    this.drivers = drivers;
    let { data: schedules } = await this.$axios.get(`/api/v1/schedules`);
    this.scheduled = schedules;
    let { data: journeys } = await this.$axios.get(`/api/v1/journeys`);
    this.journey = journeys;

    await this.structuredData();
  },
  methods: {
    assignValues({ id, bus, driver, is_active }) {
      this.travelData = {
        id,
        bus: bus.bus_plate,
        driver: driver.id,
        is_active,
      };
    },
    structuredData() {
      return new Promise((resolve, reject) => {
        this.buses.forEach((element) => {
          this.busesOptions.push({
            value: element.bus_plate,
            text: `${element.bus_plate} - capacidad: ${element.capacity}`,
          });
        });
        this.drivers.forEach((element) => {
          this.driversOptions.push({
            value: element.id,
            text: `${element.id_card} - ${element.full_name}`,
          });
        });
        this.journey.forEach((element) => {
          this.journeyOptions.push({
            value: element.id,
            text: `${element.origin} - ${element.destination}`,
          });
        });
        this.scheduled.forEach((element) => {
          this.scheduledOptions.push({
            value: element.id,
            text: `${element.departure_time}`,
          });
        });
        resolve(true);
      });
    },
    updated() {
      this.$axios
        .patch(`/api/v1/travels/${this.travel.id}`, this.travelData)
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
        this.travelData.journey != null &&
        this.travelData.scheduled != null &&
        this.travelData.bus != null &&
        this.travelData.driver != null
      ) {
        delete this.travelData.is_active;
        this.$axios
          .post(`/api/v1/travels`, this.travelData)
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
      this.$bvModal.hide("edit-travels");
    },
  },
};
</script>

<style lang="scss" scoped>
.label__select {
  text-align: start;
}
</style>