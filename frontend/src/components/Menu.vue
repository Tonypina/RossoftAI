<template>
  <aside class="p-0 col-2 surface-900 h-screen fixed z-1">
    <div id="marca" class="p-2 h-4rem surface-800">
      <div class="img-container">
        <img src="icon.png" alt="Icono">
      </div>
      <h1>Rossoft<span>AI</span></h1>
    </div>
    <ul class="px-4">
      <router-link to="/">
        <li>
          Reglas de asociación
        </li>
      </router-link>
      <router-link to="/metrics">
        <li>
          <i class="pi pi-share-alt mr-2"></i>
          Métricas
        </li>
      </router-link>
      <li class="p-0">
        <Accordion class="menu-accordion">
          <AccordionTab>
            <template #header>
              <i class="pi pi-sitemap mr-2"></i>
              Clustering
            </template>
            <ul class="p-0">
              <router-link to="/h-clust">
                <li>
                  <i class="pi pi-share-alt mr-2"></i>
                  Jerárquico
                </li>
              </router-link>
              <router-link to="/p-clust">
                <li>
                  <i class="pi pi-share-alt mr-2"></i>
                  Particional
                </li>
              </router-link>
            </ul>
          </AccordionTab>
        </Accordion>
      </li>
    </ul>
  </aside>
</template>

<script>
  import Accordion from 'primevue/accordion';
  import AccordionTab from 'primevue/accordiontab';

  export default {
    name: 'Menu',
    components: {
      Accordion,
      AccordionTab
    }
  }
</script>

<style lang="scss" scoped>

  aside {

    #marca {
      h1 {
        position: absolute;
        top: -0.3rem;
        right: 3.5rem;

        span {
          color: #F56800;
        }
      }

      .img-container {
        position: absolute;
        height: 2rem;
        top: 0;
        left: 0;
        transform: translate(50%, 50%);
  
        img {
          position: relative;
          height: 100%;
        }
      }
    }


    li {
      list-style-type: none;
      width: 100%;
      padding: 1.175rem;
      border-radius: 0.30rem;
      text-align: left;
    }

    a {
      font-weight: bold;
      color: var(--surface-50);
      text-decoration: none;

      &.router-link-exact-active {
        color: #F56800;
      }

      &:hover li {
        background-color: var(--surface-800);
        transition: all 150ms ease-in;
      }
    }

  }

  ::v-deep(.menu-accordion) {
    .p-accordion-header {
      .p-accordion-header-link {
        font-family: Exo;
        background-color: var(--surface-900);
        color: var(--surface-50);
        border: none;

        &:hover {
          background-color: var(--surface-800) !important;
          color: var(--surface-50) !important;
          transition: all 150ms ease-in;
        }

        &:focus {
          outline: none !important;
          border: none !important;
          -webkit-box-shadow: none !important;
          box-shadow: none !important;
        }
      }
    }

    .p-accordion-content {
      background-color: var(--surface-900);
      border: none;
      font-family: Exo;
    }
  }

</style>