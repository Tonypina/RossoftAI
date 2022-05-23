<template>
  <nav class="h-4rem z-5">
    <!-- <ul class="h-full px-6 mt-0 flex justify-content-center align-items-center">
      <router-link to="/">
        <li class="inline">
          <i class="pi pi-link mr-2"></i>
          Inicio
        </li>
      </router-link>
      <router-link to="/">
        <li class="inline">
          <i class="pi pi-link mr-2"></i>
          Documentación
        </li>
      </router-link>
    </ul> -->
  </nav>
</template>

<script>
  export default {
    name: 'Nav',
  }
</script>

<style lang="scss">
  nav {
    // padding: 30px;

    border-bottom: #F56800 solid 2px;
    background-color: black;

    li {
      list-style-type: none;
      width: 100%;
      padding: 1.175rem;
      border-radius: 0.30rem;
      text-align: left;
    }

    a {
      font-weight: bold;
      text-decoration: none;

      font-family: Exo;
      background-color: black;
      color: var(--surface-50);
      border: none;

      &.router-link-exact-active {
        color: #F56800;
      }
    }
  }
</style>