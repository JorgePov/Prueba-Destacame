<template>
  <div class="container parent__container">
    <form class="w-100 form__search p-2">
      <h2>Buscar Buses</h2>
      <div class="input__group">
        <b-form-input
          v-model="bus_plate"
          placeholder="Ingresar Placa"
          @keypress.capture="applyFilterBus"
        ></b-form-input>
        <b-button variant="primary" @click="resetFilter">Limpiar</b-button>
      </div>
    </form>
    <div class="travels__wrapper mt-5">
      <b-card
        no-body
        :key="index"
        class="card__travel"
        v-for="(item, index) in buses"
      >
        <b-card-header header-tag="nav">
          <b-card-text>
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="m-0">Bus</h5>
              <b-button
                style="float: right"
                @click="editBus(item)"
                variant="primary"
                >Editar</b-button
              >
            </div>
          </b-card-text>
        </b-card-header>

        <b-card-body class="text-center">
          <b-card-title>{{ item.bus_plate }}</b-card-title>
          <b-card-text> Capacidad:{{ item.capacity }} </b-card-text>
        </b-card-body>
      </b-card>
    </div>
    <div
      v-b-popover.hover.top="'Crear Bus'"
      @click="createBus"
      class="container__add mb-5"
    >
      <img width="60px" src="@/assets/img/plus.png" alt="" />
    </div>
    <EditBus :bus="data" v-on:refresh-data="fetchBus" />
  </div>
</template>

<script>
import EditBus from "@/components/layouts/modals/EditBus.vue";
export default {
  data() {
    return {
      bus_plate: "",
      busesConst: [],
      buses: [],
      data: {},
    };
  },
  mounted() {
    this.fetchBus();
  },
  methods: {
    fetchBus() {
      this.$axios.get(`/api/v1/buses`).then(({ data }) => {
        this.busesConst = [...data];
        this.buses = data;
      });
    },
    applyFilterBus() {
      const gl = this.busesConst;
      let employesFilter =  gl.filter((r) => r.bus_plate.toLowerCase() == this.bus_plate.toLowerCase() );
      if (employesFilter.length > 0) {
        this.buses = employesFilter;
      } else {
        employesFilter = [...this.busesConst];
      }
    },
    resetFilter() {
      this.buses = [...this.busesConst];
      this.bus_plate = null;
    },
    editBus(item) {
      item.id = 1;
      this.data = item;
      this.$bvModal.show("edit-bus");
    },
    createBus() {
      this.data = {};
      this.$bvModal.show("edit-bus");
    },
  },
  name: "AdminBuses",
  components: { EditBus },
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
}

.toogle__input {
  float: right;
}
</style>
