<template>
  <div class="apriori pt-5 pb-5 px-8">
    <h1 class="another-font">Módulo de Reglas de Asociación</h1>
    <div class="grid pt-5 pb-5">
      <div class="col-7 pt-2">
        <h3 class="pb-2">Ingrese la fuente de datos</h3>
        <FileUpload name="file" :customUpload="true" @uploader="uploader" chooseLabel="Elegir" uploadLabel="Subir"
          cancelLabel="Cancelar">
          <template #empty>
            <p>Suelte su archivo aquí</p>
          </template>
        </FileUpload>
      </div>
      <div class="col-5 px-4 card">
        <h3>Ingrese los parámentros del algoritmo</h3>
        <div class="p-fluid pt-3">
          <div class="field">
            <span class="p-float-label">
              <InputText id="Soporte" type="text" v-model="soporte" />
              <label for="Soporte">Soporte</label>
            </span>
          </div>
        </div>
        <div class="p-fluid pt-3">
          <div class="field">
            <span class="p-float-label">
              <InputText id="Confianza" type="text" v-model="confianza" />
              <label for="Confianza">Confianza</label>
            </span>
          </div>
        </div>
        <div class="p-fluid pt-3">
          <div class="field">
            <span class="p-float-label">
              <InputText id="Elevacion" type="text" v-model="elevacion" />
              <label for="Elevacion">Elevación</label>
            </span>
          </div>
        </div>
      </div>
    </div>
    <div class="">
      <h2>Exploración de los Datos</h2>
      <div class="">
        <DataTable :value="datos" responsiveLayout="scroll" :scrollable="true" scrollHeight="400px">
          <Column v-for="col of columns_datos" :field="col.field" :header="col.header" :key="col.field"></Column>
        </DataTable>
      </div>
      <div class="card pt-5 pb-5">
        <h2>Gráfica de Frecuencias</h2>
        <Chart type="bar" :data="Chartdatos" :options="horizontalOptions" />
      </div>
    </div>
    <div class="">
      <h2 class="pb-2">Reglas de Asociación Obtenidas</h2>
      <div class="">
        <DataTable :value="reglas" ref="dt" responsiveLayout="scroll" :scrollable="true" scrollHeight="400px">
          <template #header>
            <div style="text-align: left">
              <Button icon="pi pi-external-link" label="Exportar" @click="exportCSV($event)" />
            </div>
          </template>
          <Column v-for="col of columns_reglas" :field="col.field" :header="col.header" :key="col.field"></Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script lang="js">
  import FileUpload from 'primevue/fileupload';
  import Chart from 'primevue/chart';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import ColumnGroup from 'primevue/columngroup';
  import Row from 'primevue/row';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';

  import {
    axiosInst
  } from '../../axios-api'
  import {
    defineComponent
  } from '@vue/runtime-core';

  export default defineComponent({
    name: 'AprioriView',

    components: {
      FileUpload,
      DataTable,
      Column,
      ColumnGroup,
      Row,
      Chart,
      InputText,
      Button
    },
    data() {
      return {
        file: '',
        fileLimit: 1,
        columns_datos: null,
        columns_reglas: null,
        datos: null,
        reglas: null,
        soporte: null,
        confianza: null,
        elevacion: null,
        horizontalOptions: {
          indexAxis: 'y',
          plugins: {
            legend: {
              labels: {
                color: '#495057'
              }
            }
          },
          scales: {
            x: {
              ticks: {
                color: '#495057'
              },
              grid: {
                color: '#ebedef'
              }
            },
            y: {
              ticks: {
                color: '#495057'
              },
              grid: {
                color: '#ebedef'
              }
            }
          }
        },
        Chartdatos: null
      }
    },
    created() {
      this.columns_datos = [{
            field: 'Item',
            header: 'Item'
          },
          {
            field: 'Frecuencia',
            header: 'Frecuencia'
          },
          {
            field: 'Porcentaje',
            header: 'Porcentaje'
          }
        ],

        this.columns_reglas = [{
            field: 'items',
            header: 'Regla'
          },
          {
            field: 'support',
            header: 'Soporte'
          },
          {
            field: 'confidence',
            header: 'Confianza'
          },
          {
            field: 'lift',
            header: 'Elevación'
          },
        ]
    },
    methods: {

      exportCSV() {
        this.$refs.dt.exportCSV();
      },

      uploader(event) {

        var formData = new FormData();
        formData.append("file", event.files[0])

        axiosInst.post('/rossoftai/runAlgorithm/',
            formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Content-Disposition': 'attachment; filename=' + event.files[0].name
              }
            })
          .then(response => {
            axiosInst.get('/rossoftai/runAlgorithm/', {
              params: {
                algthm_type: "apriori",
                name: response.data,
                support: this.soporte, // 0.01
                confidence: this.confianza, // 0.3
                lift: this.elevacion // 2
              }
            }).then(response => {

              this.datos = JSON.parse(response.data[1])
              this.reglas = JSON.parse(response.data[0])

              console.log(this.reglas)

              var labelsList = new Array()
              var frequencyList = new Array()

              this.datos.forEach(element => {
                labelsList[labelsList.length] = element.Item
              })

              this.datos.forEach(element => {
                frequencyList[frequencyList.length] = element.Frecuencia
              })

              this.Chartdatos = {
                labels: labelsList,
                datasets: [{
                  label: 'Fuente de datos',
                  backgroundColor: '#F56800',
                  data: frequencyList
                }]
              }

            }).catch(error => {
              console.log(error)
            })
          })
          .catch(error => {
            console.log(error)
          });
      }
    }
  });
</script>

<style lang="scss">

  .p-button {
    background-color: #F56800;
    border: none;

    &:hover {
      background-color: #cd5702 !important;
      border: none;
    }
  }
</style>