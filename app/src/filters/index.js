import Vue from "vue";

Vue.filter('formatDate', (value) => {
  const date = new Date(value)
  return date.toLocaleString(['es-CO'], {
    month: 'long',
    day: '2-digit',
    year: 'numeric'
  })
})

Vue.filter('formatPrice', (value) => {
  return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(value)
})

Vue.filter('formatDateTime', (value) => {
  const date = new Date(value)
  return date.toLocaleString(['es-CO'], {
    month: 'long',
    day: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
})

Vue.filter('formatTime', (value) => {
  const date = new Date(value)
  return date.toLocaleString(['es-CO'], {
    hour: '2-digit',
    minute: '2-digit',
  })
})

Vue.filter('formatOnlyTime', (value) => {
  const date = new Date('July 1, 2000, ' + value)
  return date.toLocaleString(['es-CO'], {
    hour: '2-digit',
    minute: '2-digit',
  })
})
