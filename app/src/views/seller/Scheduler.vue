<template>
  <div class="container schedule__container mt-2">
    <a @click="prevStep">
      <img class="previous"
           width="50px"
           src="@/assets/img/previous.png"
           alt="">
    </a>
    <h2>Seleccion de Horario</h2>
    <form class="w-100 form__search p-2">
      <template>
        <b-form-datepicker v-model="value"
                           :min="min"
                           locale="en"
                           id="example-datepicker"
                           class="datepicker"></b-form-datepicker>
      </template>
      <b-button variant="primary"
                @click="value = today">Today</b-button>
    </form>

    <div class="schedules__wrapper mt-5">
      <b-card border-variant="primary"
              :class="item.state ? 'onTime' : 'deny'"
              class="card__travel"
              style="max-height: 15rem;"
              align="center"
              :key="index"
              @click="item.state && nextStep(item.id)"
              v-for="(item, index) in schedules">
        <b-card-text>
          {{ item.value | formatTime }}
        </b-card-text>
      </b-card>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const minDate = new Date(today)
    //sort schedule
    const scheduleId = [24, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    return {
      value: today,
      today: today,
      min: minDate,
      schedulessort: scheduleId
    }
  },
  computed: {
    user() {
      return this.$store.getters.getUser || null;
    },
    schedule() {
      return this.$store.getters['aux/getSchedule'] || [];
    },
    schedules() {
      const schedules = []
      this.schedule.sort((a, b) => this.schedulessort.indexOf(a.id) - this.schedulessort.indexOf(b.id))
      this.schedule.forEach(e => {
        schedules.push(this.structuredSchedule(e.id, e.departure_time))
      });

      schedules.map(f => f.state = new Date(f.value) > new Date())
      return schedules
    },
  },
  methods: {
    structuredSchedule(id, value) {
      const time = value.split(":")
      return { id: id, value: new Date().setHours(time[0], time[1], time[2], 0), state: false }
    },
    prevStep() {
      this.$router.push("/seller")
    },
    nextStep(index) {
      const { cases_closing, departure_time, id } = this.schedule.find(r => r.id == index);
      const dataPicked = new Date(this.value)
      let travel_date = ""
      if (dataPicked > new Date()){
        travel_date = `${this.value} ${departure_time}`
      }else{
        travel_date = `${dataPicked.getFullYear()}-${dataPicked.getMonth() + 1}-${dataPicked.getDate()} ${departure_time}`
      }
      this.$store.commit("seller/setSchedule", { travel_date, boarding_time: cases_closing })
      this.$store.commit("aux/setIdSchedule", id)
      this.$store.commit("aux/setProcessSeller", "locations")
      this.$store.commit("aux/setDate", travel_date )
      this.$store.dispatch("aux/getAxiosLocations");
      this.$router.push("/seller/locations");
    },
    recapOntime() {
      this.schedules.map(f => f.state = new Date(f.value) > new Date())
    }

  },
  watch: {
    value(value) {
      if (new Date(value) > this.today) {
        this.schedules.map(f => f.state = true)
        return
      }
      this.recapOntime()
    }
  },
  name: 'Scheduler'
}
</script>

<style lang="scss" scoped>
.datepicker {
  width: 300px;
}

.schedule__container {
  text-align: center;
}

.form__search {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.schedules__wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  align-items: center;
}

.card__travel {
  max-height: 15rem;
  max-width: 20rem;
}

.onTime {
  background-color: green;
  cursor: pointer;
}

.onTime:hover {
  background-color: yellow;
}

.deny {
  background-color: red;
}
</style>
