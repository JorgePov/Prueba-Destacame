<template>
  <div class="container">
    <form class="w-100 form__search p-2">
      <span>Consulta tus viajes:</span>
      <b-form-input placeholder="Ingresa tu cedula"  v-model="id_card"></b-form-input>
      <b-button variant="primary"  @click="getDataTravels">Consultar</b-button>
    </form>
    <div class="travels__wrapper mt-5" >
      <b-card border-variant="primary"
              class="card__travel"
              :header="`${item.travel.journey.origin} - ${item.travel.journey.destination}`"
              style="max-height: 15rem;"
              header-bg-variant="primary"
              header-text-variant="white"
              align="center"
              :key="index"
              v-for="(item, index) in travels"
              >
        <b-card-text>
          <p>Tu puesto: {{item.location_number}}</p>
          <p>Fecha: {{item.travel_date | formatDate}}</p>
          <p>Hora de salida: {{item.travel_date | formatTime}}</p>
          <p>Hora de abordaje: {{item.boarding_time | formatOnlyTime}}</p>
        </b-card-text>
      </b-card>
    </div>
    <div class="text-center" v-if="travels.length == 0 && is_fetch ">
      No se encontraron viajes comprados
    </div>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
  data() {
    return {
      travels: [],
      id_card: null,
      is_fetch: false
    }
  },
  created() {
    this.$store.commit('logout');
  },
  methods: {
    getDataTravels() {
      if (this.id_card){
        this.$axios.get(`/api/v1/locations/travelers/${this.id_card}`)
      .then(({data}) => {
        this.travels = data
      })
    }
    }
  }



}
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
