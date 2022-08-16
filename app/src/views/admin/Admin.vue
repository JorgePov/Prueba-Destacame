<template>
  <div class="container parent__container">
    <form class="w-100 form__search p-2">
      <h2>Buscar Viajes</h2>
      <div class="input__group mt-2">
        <b-form-select
          class="select__option"
          v-model="selected"
          :options="options"
          @change="applyFilterJourney"
        >
          <template #first>
            <b-form-select-option :value="null" disabled
              >Origen/Destino</b-form-select-option
            >
          </template>
        </b-form-select>
        <!-- <b-button variant="primary"
                  @click="changeSort">
          <b-icon class="custom__icon"
                  :icon="sort ? 'sort-numeric-up' : 'sort-numeric-down'"></b-icon>
          Asientos vendidos
        </b-button> -->
        <b-button variant="primary" @click="resetFilter">Limpiar</b-button>
      </div>
    </form>
    <div class="travels__wrapper mt-5">
      <b-card
        no-body
        class="card__travel"
        :key="index"
        v-for="(item, index) in travels"
      >
        <b-card-header header-tag="nav">
          <b-card-text>
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="m-0">
                {{ item.journey.origin }} - {{ item.journey.destination }}
              </h5>
              <b-button
                @click="editTravel(item)"
                style="float: right"
                variant="primary"
                >Editar</b-button
              >
            </div>
          </b-card-text>
        </b-card-header>

        <b-card-body class="text-center">
          <b-card-title>
            {{ item.scheduled.departure_time | formatOnlyTime }}</b-card-title
          >

          <b-card-text>
            <p>Bus: {{ item.bus.bus_plate }}</p>
            <p>Conductor: {{ item.driver.full_name }}</p>
          </b-card-text>
        </b-card-body>
      </b-card>
    </div>
    <div
      @click="createTravel"
      v-b-popover.hover.top="'Añadir nuevo viaje'"
      class="container__add mb-5"
    >
      <img width="60px" src="@/assets/img/plus.png" alt="" />
    </div>
    <EditTravel :travel="data" v-on:refresh-data="fetchTravels" />
  </div>
</template>

<script>
import EditTravel from "@/components/layouts/modals/EditTravel.vue";
export default {
  data() {
    return {
      selected: null,
      options: [],
      travels: [],
      travelsConst: [],
      sort: true,
      data: [],
    };
  },
  mounted() {
    this.fetchTravels();
    this.fetchJourneys();
  },
  methods: {
    fetchTravels() {
      this.$axios.get(`/api/v1/travels`).then(({ data }) => {
        this.travelsConst = [...data];
        this.travels = data;
      });
    },
    fetchJourneys() {
      this.$axios.get("/api/v1/journeys").then(({ data }) => {
        data.forEach((element) => {
          this.options.push({
            value: element.id,
            text: `${element.origin} - ${element.destination}`,
          });
        });
      });
    },
    applyFilterJourney() {
      const gl = this.travelsConst;
      this.travels = gl.filter((r) => r.journey.id == this.selected);
    },
    resetFilter() {
      this.travels = [...this.travelsConst];
    },
    changeSort() {
      this.sort = !this.sort;
    },
    editTravel(data) {
      this.data = data;
      this.$bvModal.show("edit-travels");
    },
    createTravel() {
      this.data = {};
      this.$bvModal.show("edit-travels");
    },
  },
  name: "Admin",
  components: { EditTravel },
};
</script>

<style lang="scss" scoped>
.form__search {
  input {
    width: 50%;
  }
}

.parent__container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.select__option {
  max-width: 200px;
}

.travels__wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  max-height: 500px;
  overflow: auto;
}

.card__travel {
  height: 15rem;
  max-width: 20rem;
  width: 100%;
}

.container__add {
  cursor: pointer;
  margin-top: auto;
  align-self: center;
  display: grid;
  place-items: center;
}

.input__group {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
}
</style>
