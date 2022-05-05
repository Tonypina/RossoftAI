<template>
  <div class="apriori pt-5">
    <h1>Módulo de Regresión Logística</h1>
    <div class="px-7 pt-5 pb-5">
      <FileTable v-model:dataName="this.data_name"/>
      <div class="pt-5" v-if="this.data_name">
        <div>
          <h2>Selección de Características</h2>
          <CaracSelec :dataName="this.data_name" v-model:carac="this.selectedCaracteristics"/>
        </div>
        <div>
          
        </div>
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
    name: 'RegressionView',

    components: {
      FileTable,
      CaracSelec
    },

    created() {
      this.selectedCaracteristics = []
    },

    data() {
      return {
        data_name: null,
        selectedCaracteristics: null
      }
    },

    methods: {
      
    }
  })
</script>