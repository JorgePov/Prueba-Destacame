<template>
  <div class="container">
    <a @click="prevStep">
      <img class="previous"
           width="50px"
           src="@/assets/img/previous.png"
           alt="">
    </a>
    <div class="title__travel mt-5">
      {{ }}
      <h3>{{ originDest.value }}</h3>
    </div>
    <div class="row mt-5">
      <div class="col-12 col-md-6 d-flex align-items-center justify-content-center">
        <div class="bus__container">
          <div class="buss__driver mt-2">
            <img src="@/assets/img/driver.png"
                 alt=""
                 width="80px">
          </div>
          <div class="seat__container mt-2">
            <div :key="item.id"
                 v-for="item in seats">
              <button :disabled="!item.free"
                      @click="selectesSeat(item.id)"
                      style="border: none;background: transparent;">
                <img :class="item.selected ? 'selected' : item.free ? 'free' : 'sold'"
                     width="100px"
                     src="@/assets/img/seat__top.png"
                     alt="">
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="col-12 col-md-6 mt-5 mt-md-0">
        <div class="h-100 d-flex align-items-center justify-content-center">
          <b-card no-body
                  v-if="isRegister === null"
                  class="card__travel w-100">
            <b-card-body class="text-center">
              <b-card-title>Consultar Pasajero</b-card-title>
              <b-form-input type="number"
                            placeholder="Cedula"
                            v-model="data.id_card"
                            @keypress.enter="searchTraveler"></b-form-input>
              <b-button class="mt-2 mb-0 search__button"
                        variant="primary"
                        @click="searchTraveler">Consultar</b-button>
              <b-card-text>
              </b-card-text>
            </b-card-body>
          </b-card>
          <RegisterTraveler :data="data"
                            v-on:traveler-register="travelerRegister"
                            class="w-100"
                            v-if="isRegister !== null && !isRegister" />
          <RegisterTravel :user="data"
                          :seat="selectSeat"
                          class="w-100"
                          v-if="isRegister !== null && isRegister" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import RegisterTraveler from '@/components/seller/RegisterTraveler.vue';
import RegisterTravel from '@/components/seller/RegisterTravel.vue';
export default {
  data() {
    return {
      seats: [],
      selectSeat: 0,
      isRegister: null,
      queryTraveler: true,
      id_card: null,
      data: {
        id_card: null,
        first_name: null,
        last_name: null,
        age: null
      }
    };
  },
  computed: {
    user() {
      return this.$store.getters.getUser || null;
    },
    capacity() {
      return this.$store.getters['aux/getCapacity'] || 10;

    },
    locations() {
      return this.$store.getters['aux/getLocations'];

    },
    originDest() {
      return this.$store.getters['aux/getJourney'] || [];
    },

  },
  mounted() {
    this.structuredBus()
  },
  watch: {
    locations(value) {
      const seatTaking = value.map(({ location_number }) => location_number)
      this.seats.map(f => {
        if (seatTaking.includes(f.id)) {
          f.free = false
        }
      })
    }
  },
  methods: {
    structuredBus() {
      for (let i = 1; i < this.capacity + 1; i++) {
        this.seats.push({ id: i, free: true, selected: false })
      }
    },
    prevStep() {
      this.$store.commit("aux/setProcessSeller", "schedulers")
      this.$store.dispatch("aux/getAxiosSchedules");
      this.$router.push("/seller/schedulers")
    },
    selectesSeat(id) {
      if (!this.seats.find(f => f.id === id).free) {
        const data = {
          variant: "danger",
          text: "Esta silla ya se encuentra registrada",
          seconds: 4
        };
        this.$store.commit("alerts/setAlert", data);
        return;
      }
      this.seats.filter(f => f.id === id ? f.selected = true : f.selected = false);
      this.selectSeat = id;
      this.$store.commit("seller/setLocation_number", id)
    },
    searchTraveler() {
      this.$axios.get(`/api/v1/travelers/${this.data.id_card}`).then(({ data }) => {
        this.data = data;
        this.$store.commit("seller/setTraveler", data.id_card)
        this.isRegister = true
      }).catch((err) => {
        this.isRegister = false
      });;
    },
    travelerRegister(data) {
      this.$axios
        .post("/api/v1/travelers", data)
        .then(({ data }) => {
          this.data = data;
          this.$store.commit("seller/setTraveler", data.id_card)
          this.isRegister = true
        });
    }
  },
  name: "Location",
  components: { RegisterTraveler, RegisterTravel }
}
</script>

<style lang="scss" scoped>
.free {
  filter: invert(29%) sepia(95%) saturate(1076%) hue-rotate(88deg) brightness(94%) contrast(111%);
}

.sold {
  filter: invert(13%) sepia(94%) saturate(4448%) hue-rotate(353deg) brightness(99%) contrast(124%);
}

.selected {
  filter: invert(89%) sepia(16%) saturate(1077%) hue-rotate(338deg) brightness(106%) contrast(102%);
}

.bus__container {
  border: 1px solid;
  border-radius: 10px;
  width: 250px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: lightgrey;
  overflow: hidden;
}

.search__button {
  float: right !important;
}

.buss__driver {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.seat__container {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
}

.title__travel {
  text-align: center;
}
</style>
