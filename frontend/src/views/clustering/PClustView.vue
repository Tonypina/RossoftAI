<template>
  <div class="apriori pt-5">
    <h1>Módulo de Clustering Particional</h1>
    <div class="px-7 pt-5 pb-5">
      <FileTable v-model:dataName="this.data_name" />
      <div class="pt-5" v-if="this.data_name">
        <h2>Selección de Características</h2>
        <CaracSelecClust clustType="kmeans" :dataName="this.data_name" v-model:sse="this.lineChartData.datasets[0].data"
          v-model:elbow="this.elbow" v-model:carac="this.selectedCarac" />
        <div v-if="this.lineChartData.datasets[0].data.length">
          <h2>Método del codo</h2>
          <div class="grid">
            <div class="col-8">
              <Chart type="line" :data="lineChartData" />
            </div>
            <div class="col-4">
              <h3>Inserte el número de clusters que utilizará</h3>
              <h4>Recomendación: {{this.elbow}}</h4>
              <div class="grid">
                <div class=col-10>
                  <InputText id="nClust" placeholder="Número de Clusters" v-model="this.nClust" />
                </div>
                <div class="col-2">
                  <Button icon="pi pi-check" iconPos="right" @click="sendNumClust" />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="pt-5" v-if="this.centroides.length > 0">
          <h2>Clusters obtenidos</h2>
          <Centroides :centroides="this.centroides" :dataClust="this.data_clust"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="js">
  import FileTable from '../../components/FileTable'
  import CaracSelecClust from '../../components/CaracSelecClust'
  import Centroides from '../../components/Centroides'
  import Chart from 'primevue/chart'
  import InputText from 'primevue/inputtext'
  import Button from 'primevue/button'

  import {
    defineComponent
  } from '@vue/runtime-core';

  import {axiosInst} from '../../axios-api'

  export default defineComponent({
    name: 'PClustView',

    components: {
      FileTable,
      CaracSelecClust,
      Centroides,
      Chart,
      InputText,
      Button
    },

    created() {
      this.centroides = [],
        this.data_clust = [],
        this.elbow,
        this.nClust,
        this.selectedCarac = []
    },

    data() {
      return {
        data_name: null,
        centroides: null,
        data_clust: null,
        elbow: null,
        nClust: null,
        selectedCarac: null,

        lineChartData: {
          labels: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          datasets: [{
            label: 'SSE',
            data: [],
            fill: false,
            borderColor: '#42A5F5',
            tension: 0
          }]
        }
      }
    },

    methods: {

      sendNumClust() {
        
        axiosInst.get('/rossoftai/runAlgorithm/', {
          params: {
            name: this.data_name,
            algthm_type: 'pclust',
            nClust: this.nClust,
            carac: JSON.stringify(this.selectedCarac)
          }
        }).then(res => {

          this.data_clust = JSON.parse(res.data[0])
          this.centroides = JSON.parse(res.data[1])

        }).catch(err => console.log(err))
      }
    }
  })
</script>