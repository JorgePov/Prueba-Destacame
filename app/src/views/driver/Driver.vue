<template>
  <div class="container">
    <h2>{{ user.first_name }}, Tus rutas asignadas</h2>
    <div class="travels__wrapper mt-5">
      <b-card
        border-variant="primary"
        class="card__travel"
        :header="`${item.journey.origin} - ${item.journey.destination}`"
        style="max-height: 15rem"
        header-bg-variant="primary"
        header-text-variant="white"
        align="center"
        :key="index"
        v-for="(item, index) in travels"
      >
        <b-card-text> 
          <p>Bus: {{item.bus.bus_plate}}</p>
          <p>Hora de salida: {{item.scheduled.departure_time | formatOnlyTime}}</p>
        </b-card-text>
      </b-card>
    </div>
    <div class="text-center" v-if="travels.length == 0">
      No tienes rutas asignadas
    </div>
  </div>
</template>

<script>
export default {
  name: "Driver",
  data() {
    return {
      travels: [],
    };
  },
  computed: {
    user() {
      return this.$store.getters.getUser || null;
    },
  },
  async mounted() {
    if(this.user.id){
      await this.getDataTravels();
    }else{
      await this.getDataTravels();
    }
  },
  methods: {
    getDataTravels() {
      this.$axios
        .get(`/api/v1/driver/travels/${this.user.id}`)
        .then(({ data }) => {
          this.travels = data;
        })
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
  place-items: center;

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
