<template>
  <div>
    <b-card no-body
            class="card__travel">
      <b-card-body class="card__body">
        <b-card-title>Detalle de reserva</b-card-title>
        <div class="text__center">
          <p><span class="label__form">Nombre pasajero:&nbsp;</span> {{ `${user.first_name} ${user.last_name}` }}</p>
          <p><span class="label__form">Cedula:&nbsp;</span>{{ data.traveler }}</p>
          <p><span class="label__form">Hora viaje:&nbsp;</span> {{ data.travel_date | formatDateTime }}</p>
          <p><span class="label__form">Precio:&nbsp;</span> {{ travel.journey.price | formatPrice }}</p>
          <div class="d-flex align-items-center justify-content-center">
            <h2><span class="label__form">Puesto:&nbsp;</span>{{ data.location_number || seat }}</h2>
          </div>
        </div>
        <b-button class="mt-2 mb-0 search__button"
                  variant="primary"
                  @click="createLocation">Reservar</b-button>
      </b-card-body>
    </b-card>
  </div>
</template>
<script>
export default {
  props: ['seat', 'user'],
  computed: {
    data() {
      return this.$store.getters['seller/getLocation'];
    },
    travel() {
      return this.$store.getters['aux/getTravels'].find(r=>r.id ==this.data.travel);
    }
  },
  methods: {
    createLocation() {
      if (this.seat > 0) {
        this.$axios
          .post("/api/v1/locations", this.data)
          .then(({ data }) => {
            this.isRegister = true
            this.$store.commit("aux/reset")
            this.$store.commit("seller/reset")
            this.$router.push("/seller");
          });
      } else {
        this.$store.commit("alert/setAlert", {
          variant: "danger",
          text: "Selecciona una silla",
          seconds: 3,
        });
      }
    }
  }
}
</script>

<style lang="scss">
.card__travel {
  width: 30rem;
  max-width: 50rem;
}

.text__center {
  text-align: center;

  &>p {
    text-align: left;
  }
}

.label__form {
  font-weight: 500;
}
</style>
