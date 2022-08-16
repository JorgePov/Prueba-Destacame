<template>
  <div class="container">
    <form class="w-100 form__search p-2">
      <b-form-select
        class="select__option"
        v-model="selected"
        :options="options"
        @change="applyFilterJourney"
      >
        <template #first>
          <b-form-select-option :value="null" disabled
            >Trayecto</b-form-select-option
          >
        </template>
      </b-form-select>

      <!-- <b-button variant="primary" @click="changeSort">
        <b-icon
          class="custom__icon"
          :icon="sort ? 'sort-numeric-up' : 'sort-numeric-down'"
        ></b-icon>
        Asientos vendidos
      </b-button> -->
      <b-button variant="primary" @click="resetFilter">Clear</b-button>
    </form>
    <div class="travels__wrapper mt-5">
      <b-card
        no-body
        class="card__travel"
        :key="index"
        v-for="(item, index) in travels"
      >
        <b-card-header header-tag="nav">
          <b-card-text> {{item.origin}} - {{item.destination}} </b-card-text>
        </b-card-header>

        <b-card-body class="text-center">

          <b-card-text>
            Informacion de venta
          </b-card-text>
        </b-card-body>
        <template #footer class="d-flex">
          <div class="d-flex justify-content-between">
            <p class="m-0 align-self-center">Precio venta: {{item.price | formatPrice}}</p>
            <b-button style="float: right" variant="primary" @click="nextStep(item.id)">Vender</b-button>
          </div>
        </template>
      </b-card>
    </div>
  </div>
</template>

<script>
export default {
  name: "Seller",
  data() {
    return {
      selected: null,
      options: [],
      travels: [],
      travelsConst: [],
      sort: true,
    };
  },
  computed: {
    user() {
      return this.$store.getters.getUser || null;
    },
  },

  mounted() {
      this.getDataTravels();
      this.fetchJourneyData();
      
  },

  methods: {
    getDataTravels() {
      this.$axios
        .get(`/api/v1/travels`)
        .then(({ data }) => {
          this.$store.commit("aux/setTravels",data);
        });
    },
    fetchJourneyData() {
      this.$axios.get('/api/v1/journeys')
        .then(({ data }) => {
          this.travelsConst = [... data];
          this.travels = data;
          data.forEach(element => {
            this.options.push({value:element.id,  text: `${element.origin} - ${element.destination}`})
          });
        });
    },
    applyFilterJourney() {
      const gl =  this.travelsConst
      this.travels = gl.filter(r=> r.id == this.selected)
    },
    resetFilter() {
      this.travels =  [ ...this.travelsConst]
    },
    nextStep(id) {
      let { text } = this.options.find(r=> r.value == id);
      this.$store.commit("aux/setJourney",{id: id, value: text})
      this.$store.commit("aux/setProcessSeller","schedulers")
      this.$store.dispatch("aux/getAxiosSchedules");
      this.$router.push("/seller/schedulers");
    },
    changeSort() {
      this.sort = !this.sort;
      
    },
  },
};
</script>

<style lang="scss" scoped>
.form__search {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;

  input {
    width: 50%;
  }
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
}

.card__travel {
  height: 15rem;
  max-width: 20rem;
  width: 100%;
}

</style>
