<template>
  <div class="grid">
    <Menu/>
    <div class="p-0 col-9 col-offset-3 fixed top-0 z-5">
      <Nav/>
    </div>
    <div class="p-0 col-9 col-offset-3 mt-7 z-1">
      <router-view/>
    </div> 
  </div>
</template>

<style lang="scss">
@import "~primeflex/primeflex.css";
@import url('https://fonts.googleapis.com/css2?family=Montserrat&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Exo:wght@100&display=swap');

#app {
  // font-family: Avenir, Helvetica, Arial, sans-serif;
  font-family: 'Exo', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: black;
}
</style>

<script>
  import Menu from './components/Menu.vue'
  import Nav from './components/Nav.vue'

  export default {
    components: {
      Menu,
      Nav
    }
  }
</script>
