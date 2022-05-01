<template>
  <nav class="h-4rem bg-white shadow-5 z-5">

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
  box-shadow: 0px 5px 6px 0px rgba(194,194,194,0.53);
  -webkit-box-shadow: 0px 5px 6px 0px rgba(194,194,194,0.53);
  -moz-box-shadow: 0px 5px 6px 0px rgba(194,194,194,0.53);

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #F56800;
    }
  }
}
</style>