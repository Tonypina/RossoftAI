<template>
  <div class="apriori pt-5">
    <h1>Módulo de Clustering Jerárquico</h1>
    <div class="px-7 pt-5 pb-5">
      <FileTable v-model:dataName="this.data_name"/>
      <div v-if="this.data_name">
        <h2>Selección de Características</h2>
        <CaracSelec :dataName="this.data_name"/>        
      </div>
    </div>
  </div>
</template>

<script lang="js">
  import FileTable from '../components/FileTable'
  import CaracSelec from '../components/CaracSelec'
  // import Chart from 'primevue/chart';

  import { defineComponent } from '@vue/runtime-core';

  export default defineComponent({
    name: 'HClustView',

    components: {
      FileTable,
      CaracSelec
    },
    
    data() {
      return {
        data_name: null,
      }
    },

    methods: {
      
    }
  })
</script>