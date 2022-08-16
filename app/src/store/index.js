import Vue from "vue";
import Vuex from "vuex";
import Axios from "@/services/axios";
Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    token: null,
    user: {},
    rol: "guest",
  },
  getters: {
    getToken(state) {
      return state.token;
    },
    getUser(state) {
      return state.user;
    },
    getRol(state) {
      return state.rol;
    },
  },
  mutations: {
    setToken(state, token) {
      localStorage.setItem("token", token);
      state.token = token;
    },
    setRol(state) {
      if (state.user.is_driver) {
        state.rol = "driver";
        localStorage.setItem("rol", "driver");
      } else if (state.user.is_seller) {
        state.rol = "seller";
        localStorage.setItem("rol", "seller");
      } else if (state.user.is_staff) {
        state.rol = "admin";
        localStorage.setItem("rol", "admin");
      }
    },
    setUser(state, user) {
      state.user = user;
    },
    logout(state) {
      (state.token = null), (state.user = {}), (state.rol = "guest");
      localStorage.clear();
    },
  },
  actions: {
    async setCurrentUser({ commit }) {
      let { data } = await Axios.get("/api/v1/users");
      commit("setUser", data);
    },
  },
});

store.registerModule("alert", {
  namespaced: true,
  state: {
    variant: "",
    text: "",
    seconds: 0,
  },
  getters: {
    getVariant(state) {
      return state.variant;
    },
    getText(state) {
      return state.text;
    },
    getCount(state) {
      return state.seconds;
    },
  },
  mutations: {
    setAlert(state, { variant, text, seconds }) {
      state.variant = variant;
      state.text = text;
      state.seconds = seconds;
    },
    reset(state) {
      state.variant = "";
      state.text = "";
      state.seconds = 0;
    },
  },
});

store.registerModule("aux", {
  namespaced: true,
  state: {
    processSeller: "journey",
    travels: [],
    journey: {},
    datePicket: false,
    idSchedule: 0,
    traveler: {},
    schedule: [],
    locations: [],
    capacity: 10,
    isRegister: null,
    drivers:[],
    buses: []
  },
  getters: {
    getDrivers(state) {
      return state.drivers;
    },
    getBuses(state) {
      return state.buses;
    },
    getSchedule(state) {
      return state.schedule;
    },
    getCapacity(state) {
      return state.capacity;
    },
    getLocations(state) {
      return state.locations;
    },
    getIdSchedule(state) {
      return state.idSchedule;
    },
    getJourney(state) {
      return state.journey;
    },
    getProcessSeller(state) {
      return state.processSeller;
    },
    getIsRegister(state) {
      return state.isRegister;
    },
    getTravels(state) {
      return state.travels;
    },
    getDate(state) {
      return state.datePicket;
    },
  },
  mutations: {
    setDate(state, datePicket) {
      state.datePicket = datePicket
    },
    setDrivers(state, drivers) {
      state.drivers = drivers
    },
    setBuses(state, buses) {
      state.buses = buses;
    },
    setTraveler(state, traveler) {
      state.traveler = traveler
    },
    setSchedule(state, schedule) {
      state.schedule = schedule;
    },
    setCapacity(state, capacity) {
      state.capacity = capacity;
    },
    setLocations(state, locations) {
      state.locations = locations;
    },
    setJourney(state, journey) {
      state.journey = journey;
    },
    setIsRegister(state, isRegister) {
      state.isRegister = isRegister;
    },
    setIdSchedule(state, idSchedule) {
      state.idSchedule = idSchedule;
    },
    setProcessSeller(state, processSeller) {
      state.processSeller = processSeller;
    },
    setTravels(state, travels) {
      state.travels = travels;
    },
    reset(state) {
      state.processSeller = "journey";
      state.travels = [];
      state.journey = {};
      state.idSchedule = 0;
      state.schedule = [];
      state.locations = [];
      state.capacity = 10;
      state.isRegister = null;
    },
  },
  actions: {
    async getAxiosSchedules({ commit, state }) {
      let { data } = await Axios.get(`/api/v1/schedules/${state.journey.id}`);
      commit("setSchedule", data);
    },
    async getAxiosLocations({ rootState, state, commit }) {
      let { id, bus } = state.travels.find(
        (r) =>
          r.scheduled.id == state.idSchedule && r.journey.id == state.journey.id
      );
      let { data } = await Axios.post(`/api/v1/locations/travel/${id}`,{ date: state.datePicket});
      commit("setCapacity", bus.capacity);
      rootState.seller.data.travel = id;
      commit("setLocations", data);
    },
    async fetchDataAdmin({ commit, state }) {
      let { data: buses } = await Axios.get(`/api/v1/buses`);
      commit("setBuses", buses);
      let { data: drivers } = await Axios.get(`/api/v1/drivers`);
      commit("setDrivers", drivers);
      let { data: schedules } = await Axios.get(`/api/v1/schedules`);
      commit("setSchedule", schedules);
      let { data: journeys } = await Axios.get(`/api/v1/journeys`);
      commit("setJourney", journeys);
    },
  },
});

store.registerModule("seller", {
  namespaced: true,
  state: {
    data: {
      travel: null,
      traveler: null,
      location_number: null,
      travel_date: null,
      boarding_time: null,
    },
  },
  getters: {
    getLocation(state) {
      return state.data;
    },
  },
  mutations: {
    setSchedule(state, { travel_date, boarding_time }) {
      state.data.boarding_time = boarding_time;
      state.data.travel_date = travel_date;
    },
    setTravel(state, travel) {
      state.data.travel = travel;
    },
    setTraveler(state, traveler) {
      state.data.traveler = traveler;
    },
    setLocation_number(state, location_number) {
      state.data.location_number = location_number;
    },
    reset(state) {
      state.data = {
        travel: null,
        traveler: null,
        location_number: null,
        travel_date: null,
        boarding_time: null,
      };
    },
  },
});

export default store;
