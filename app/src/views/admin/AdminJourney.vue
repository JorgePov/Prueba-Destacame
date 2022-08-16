<template>
  <div class="container parent__container">
    <form class="w-100 form__search p-2">
      <h2>Buscar Trayectos</h2>
      <div class="input__group">
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
            <div class="d-flex justify-content-end align-items-center">
              
              <b-button
                @click="editJourney(item)"
                style="float: right"
                variant="primary"
                >Editar</b-button
              >
            </div>
          </b-card-text>
        </b-card-header>

        <b-card-body class="text-center">
          <b-card-title>{{ item.origin }} - {{ item.destination }}</b-card-title>

          <b-card-text> Precio : {{item.price | formatPrice}} </b-card-text>
        </b-card-body>
      </b-card>
    </div>
    <div v-b-popover.hover.top="'Crear trayecto'" class="container__add mb-5" @click="createJourney">
      <img width="60px" src="@/assets/img/plus.png" alt="" />
    </div>
    <EditJourney :journey="data" v-on:refresh-data="fetchJourneys" />
  </div>
</template>

<script>
import EditJourney from "@/components/layouts/modals/EditJourney.vue";
export default {
  data() {
    return {
      selected: null,
      options: [],
      sort: true,
      travels: [],
      travelsConst: [],
      data: [],
    };
  },
  mounted() {
    this.fetchJourneys();
  },
  methods: {
    fetchJourneys() {
      this.$axios.get("/api/v1/journeys").then(({ data }) => {
        this.travelsConst = [...data];
        this.travels = data;
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
      this.travels = gl.filter((r) => r.id == this.selected);
    },
    resetFilter() {
      this.travels = [...this.travelsConst];
    },
    editJourney(data) {
      this.data = data;
      this.$bvModal.show("edit-journey");
    },
    createJourney() {
      this.data = {};
      this.$bvModal.show("edit-journey");
    },
  },
  name: "AdminBuses",
  components: { EditJourney },
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

.toogle__input {
  float: right;
}
</style>
