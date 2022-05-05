<template>
  <div class="apriori pt-5">
    <h1>Módulo de Clustering Jerárquico</h1>
    <div class="px-7 pt-5 pb-5">
      <FileTable v-model:dataName="this.data_name"/>
      <div class="pt-5" v-if="this.data_name">
        <h2>Selección de Características</h2>
        <CaracSelec :dataName="this.data_name" v-model:centroides="this.centroides" v-model:dataClust="this.data_clust"/>
        <div class="pt-5" v-if="this.centroides.length > 0">
          <h2>Clusters obtenidos</h2>
          <Centroides :centroides="this.centroides" :dataClust="this.data_clust"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="js">
  import FileTable from '../components/FileTable'
  import CaracSelec from '../components/CaracSelec'
  import Centroides from '../components/Centroides'
  // import Chart from 'primevue/chart';

  import { defineComponent } from '@vue/runtime-core';

  export default defineComponent({
    name: 'HClustView',

    components: {
      FileTable,
      CaracSelec,
      Centroides
    },

    created() {
      this.centroides = []
      this.data_clust = []
    },

    data() {
      return {
        data_name: null,
        centroides: null,
        data_clust: null
      }
    },

    methods: {
      
    }
  })
</script>