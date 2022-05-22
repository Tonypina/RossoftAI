<template>
  <div class="apriori pt-5">
    <h1>Módulo de Clustering Jerárquico</h1>
    <div class="px-7 pt-5 pb-5">
      <FileTable v-model:dataName="this.data_name" />
      <div class="pt-5" v-if="this.data_name">
        <h2>Selección de Características</h2>
        <CaracSelecClust clustType="hclust" :dataName="this.data_name" v-model:centroides="this.centroides"
          v-model:dataClust="this.data_clust" />
        <div class="pt-5" v-if="this.centroides.length > 0">
          <Button label="Mostrar datos con etiqueta" @click="show_clust" />
          <div v-if="this.show_clust_bool">
            <h2>Datos con etiquetas</h2>
            <DataTable :value="data_clust" ref="dt" responsiveLayout="scroll" :scrollable="true" scrollHeight="400px">
              <template #header>
                <div style="text-align: left">
                  <Button icon="pi pi-external-link" label="Exportar" @click="exportCSV($event)" />
                </div>
              </template>
              <Column v-for="col of columns_data_clust" :field="col.field" :header="col.header" :key="col.field">
              </Column>
            </DataTable>
          </div>
          <div class="pt-5">
            <h2>Clusters obtenidos</h2>
            <Centroides :centroides="this.centroides" :dataClust="this.data_clust" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="js">
  import FileTable from '../../components/FileTable'
  import CaracSelecClust from '../../components/CaracSelecClust'
  import Centroides from '../../components/Centroides'
  import DataTable from 'primevue/datatable'
  import Column from 'primevue/column'
  import Button from 'primevue/button'

  import {
    defineComponent
  } from '@vue/runtime-core';

  export default defineComponent({
    name: 'HeriarchyView',

    components: {
      FileTable,
      CaracSelecClust,
      Centroides,
      DataTable,
      Column,
      Button
    },

    created() {
      this.centroides = []
      this.data_clust = []
      this.columns_data_clust = []
      this.show_clust_bool = false
    },

    data() {
      return {
        data_name: null,
        centroides: null,
        data_clust: null,
        columns_data_clust: null,
        show_clust_bool: null
      }
    },

    methods: {
      show_clust() {
        var headersList = Object.keys(this.data_clust[0])

        for (let i = 0; i < headersList.length; i++) {
          this.columns_data_clust[i] = {
            field: headersList[i],
            header: headersList[i]
          }
        }

        this.show_clust_bool = true
      },

      exportCSV() {
        this.$refs.dt.exportCSV();
      }
    }
  })
</script>