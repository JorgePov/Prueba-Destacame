<template>
  <b-sidebar id="sidebar"
             backdrop-variant="dark"
             backdrop
             shadow>
    <div class="px-3 py-2">
      <ul>
        <li>
          <router-link active-class="active"
                       to="/admin">Viajes</router-link>
        </li>
        <li>
          <router-link active-class="active"
                       to="/admin/buses">Buses</router-link>
        </li>
        <li>
          <router-link active-class="active"
                       to="/admin/journeys">Trayectos</router-link>
        </li>
        <li>
          <router-link active-class="active"
                       to="/admin/employes">Empleados</router-link>
        </li>
      </ul>
    </div>
  </b-sidebar>
</template>

<script>
export default {
  name: 'Sidebar'
}
</script>

<style lang="scss">
ul {
  list-style-type: none;
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 0;
}

li>a {
  font-weight: 500;
  color: black;
  text-decoration: none;
}
</style>
