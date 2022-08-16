<template>
  <div class="container parent__container">
    <form class="w-100 form__search p-2">
      <h2>Buscar Empleados</h2>
      <div class="input__group">
        <b-form-input
          placeholder="Cedula"
          v-model="selected"
          @keypress.capture="applyFilterEmployes"
        ></b-form-input>

        <b-button variant="primary" @click="resetFilter">Limpiar</b-button>
      </div>
    </form>
    <div class="travels__wrapper mt-5">
      <b-card
        v-for="(item, index) in employes"
        no-body
        :key="index"
        class="card__travel"
      >
        <b-card-body class="text-center">
          <b-card-title>{{ item.full_name }}</b-card-title>
          <b-card-text>
            <p style="text-align: left">
              <b>Cedula:</b> {{ item.id_card }}
              <br />
              <b>Nombre:</b> {{ item.first_name }}
              <br />
              <b>Apellido:</b> {{ item.last_name }}
              <br />
              <b>Email:</b> {{ item.email }}
              <br />
              <b>edad:</b> {{ item.age }}
            </p>
          </b-card-text>
        </b-card-body>
        <template #footer>
          <div class="d-flex justify-content-around">
            <b-button variant="danger" @click="deleteEmploye(item.id)">Eliminar</b-button>
            <b-button @click="editEmploye(item)" variant="primary"
              >Editar</b-button
            >
          </div>
        </template>
      </b-card>
    </div>
    <button
      @click="createEmploye"
      v-b-popover.hover.top="'agregar nuevo empleado'"
      class="container__add mb-5"
    >
      <img width="60px" src="@/assets/img/plus.png" alt="" />
    </button>
    <EditEmploye :employe="data" v-on:refresh-data="fetchEmployes" />
  </div>
</template>

<script>
import EditEmploye from "@/components/layouts/modals/EditEmploye.vue";
export default {
  data() {
    return {
      employes: [],
      employesConst: [],
      selected: null,
      data: {},
      sort: true,
    };
  },
  mounted() {
    this.fetchEmployes();
  },
  methods: {
    fetchEmployes() {
      this.$axios.get(`/api/v1/employes`).then(({ data }) => {
        this.employesConst = [...data];
        this.employes = data;
      });
    },
    applyFilterEmployes() {
      const gl = this.employesConst;
      let employesFilter = gl.filter((r) => r.id_card == this.selected);
      if (employesFilter.length > 0) {
        this.employes = employesFilter;
      } else {
        employesFilter = [...this.employesConst];
      }
    },
    resetFilter() {
      this.employes = [...this.employesConst];
      this.selected = null;
    },
    changeSort() {
      this.sort = !this.sort;
    },
    editEmploye(item) {
      this.data = item;
      this.$bvModal.show("edit-employe");
    },
    createEmploye() {
      this.data = {};
      this.$bvModal.show("edit-employe");
    },
    deleteEmploye(id){
      this.$axios
          .delete(`/api/v1/users/${id}`)
          .then((res) => {
            this.fetchEmployes()
          })
          .catch(({ response }) => {
            if (response) {
              this.$store.commit("alert/setAlert", {
                variant: "danger",
                text: response.data.res,
                seconds: 3,
              });
            }
          });
    }
  },
  name: "AdminBuses",
  components: { EditEmploye },
};
</script>

<style lang="scss" scoped>
.form__search {
  input {
    width: 20%;
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
  max-width: 20rem;
  width: 100%;
}

.container__add {
  margin-top: auto;
  align-self: center;
  display: grid;
  place-items: center;
  background: transparent;
  border: none;
}

.input__group {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
}

.toogle__input {
  display: flex;
  justify-content: space-between;
  align-items: center;
  float: right;
  gap: 20px;
}
</style>
