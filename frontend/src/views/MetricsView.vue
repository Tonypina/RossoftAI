<template>
  <div class="metrics pt-5 pb-5 px-8">
    <h1>Módulo de <span>Métricas</span></h1>
    <h3>Ingrese la fuente de datos</h3>
    <FileUpload name="file" :customUpload="true" @uploader="uploader" chooseLabel="Elegir" uploadLabel="Subir"
      cancelLabel="Cancelar">
      <template #empty>
        <p>Suelte su archivo aquí</p>
      </template>
    </FileUpload>
    <h2>Datos</h2>
    <DataTable :value="datos" responsiveLayout="scroll" :scrollable="true" scrollHeight="400px">
      <Column v-for="col of columns_datos" :field="col.field" :header="col.header" :key="col.field"></Column>
    </DataTable>
    <div class="pt-7" v-if="this.data_name">
      <TabView>
        <TabPanel header="Matriz de Distancias">
          <div class="pt-2">
            <h3>Seleccione la métrica</h3>
            <div class="grid pt-3">
              <div class="col-9">
                <div v-for="metric of metrics" :key="metric.key" class="inline px-4">
                  <RadioButton :id="metric.key" name="metric" :value="metric" v-model="selectedMetric" />
                  <label :for="metric.key" class="px-2">{{metric.name}}</label>
                </div>
              </div>
              <div class="col-3">
                <div v-if="selectedMetric.key == 'minkowski'">
                  <div class="p-inputgroup">
                    <span class="p-inputgroup-addon">
                      <i class="font-semibold">λ</i>
                    </span>
                    <InputText placeholder="Parámetro lambda" v-model="lambda" />
                  </div>
                </div>
              </div>
            </div>
            <div class="p-5">
              <Button label="Obtener matriz" @click="getDistances" />
            </div>
            <h3>Matriz generada</h3>
            <DataTable :value="distancias" :lazy="true" responsiveLayout="scroll" :scrollable="true"
              scrollHeight="400px">
              <Column v-for="col of columns_distancias" :field="col.field" :header="col.header" :key="col.field">
              </Column>
            </DataTable>
          </div>
        </TabPanel>
        <TabPanel header="Distancias entre objetos">
          <div class="pt-2">
            <h3>Seleccione la métrica</h3>
            <div class="grid pt-3">
              <div class="col-9">
                <div v-for="metric of metrics" :key="metric.key" class="inline px-4">
                  <RadioButton :id="metric.key" name="metric" :value="metric" v-model="selectedMetric" />
                  <label :for="metric.key" class="px-2">{{metric.name}}</label>
                </div>
              </div>
              <div class="col-3">
                <div v-if="selectedMetric.key == 'minkowski'">
                  <div class="p-inputgroup">
                    <span class="p-inputgroup-addon">
                      <i class="font-semibold">λ</i>
                    </span>
                    <InputText placeholder="Parámetro lambda" v-model="lambda" />
                  </div>
                </div>
              </div>
            </div>
            <div class="p-4">
              <h3 class="pb-3">Seleccione los objetos</h3>
              <div class="px-3 inline">
                <Dropdown v-model="selectedObject1" :options="objects" optionLabel="name" placeholder="Selecciona un objeto" />
              </div>
              <div class="px-3 inline">
                <Dropdown v-model="selectedObject2" :options="objects" optionLabel="name" placeholder="Selecciona un objeto" />
              </div>
              <Button label="Obtener distacia" @click="getDistance" />
            </div>
            <label class="px-3">La distancia calculada es: {{ calculatedDistance }}</label>
          </div>
        </TabPanel>
      </TabView>
    </div>
  </div>
</template>

<script>
  import FileUpload from 'primevue/fileupload';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Row from 'primevue/row';
  import TabView from 'primevue/tabview';
  import TabPanel from 'primevue/tabpanel';
  import RadioButton from 'primevue/radiobutton';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button'
  import Dropdown from 'primevue/dropdown';

  import {
    axiosInst
  } from '../axios-api';

  export default {
    name: 'MetricsView',

    components: {
      FileUpload,
      DataTable,
      Column,
      Row,
      TabView,
      TabPanel,
      RadioButton,
      InputText,
      Button,
      Dropdown
    },

    data() {
      return {
        data_name: '',
        datos: [],
        columns_datos: [],
        distancias: [],
        columns_distancias: [],
        metrics: [{
            name: 'Euclidea',
            key: 'euclidean'
          },
          {
            name: 'Chebyshev',
            key: 'chebyshev'
          },
          {
            name: 'Manhattan',
            key: 'cityblock'
          },
          {
            name: 'Minkowski',
            key: 'minkowski'
          }
        ],
        selectedMetric: null,
        lambda: null,
        objects: [],
        selectedObject1: null,
        selectedObject2: null,
        calculatedDistance: null
      }
    },

    created() {
      this.selectedMetric = this.metrics[0]
    },

    methods: {
      uploader(event) {

        var formData = new FormData();
        formData.append("file", event.files[0])

        axiosInst.post('/rossoftai/runAlgorithm/',
            formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Content-Disposition': 'attachment; filename=' + event.files[0].name
              }
            }
          ).then(response => {
            this.data_name = response.data

            axiosInst.get('/rossoftai/runAlgorithm/', {
              params: {
                algthm_type: "get_data",
                name: this.data_name,
              }
            }).then(response => {

              var dataList = JSON.parse(response.data)
              var headersList = Object.keys(dataList[0])

              for (let i = 0; i < headersList.length; i++) {
                this.columns_datos[i] = {
                  field: headersList[i],
                  header: headersList[i]
                }
                this.objects[i] = {
                  name: headersList[i],
                  value: i
                }
              }
              this.datos = dataList

            }).catch(function (error) {
              console.log(error)
            })
          })
          .catch(error => console.log(error))
      },

      getDistances(event) {

        axiosInst.get('/rossoftai/runAlgorithm/', {
          params: {
            algthm_type: "metrics",
            metric: this.selectedMetric.key,
            lambda: this.lambda,
            name: this.data_name
          }
        }).then(response => {

          var distaceMatrix = JSON.parse(response.data)
          var headersList2 = Object.keys(distaceMatrix[0])

          for (let i = 0; i < headersList2.length; i++) {
            this.columns_distancias[i] = {
              field: headersList2[i],
              header: headersList2[i]
            }
          }
          console.log(this.columns_distancias)
          this.distancias = distaceMatrix

        }).catch(error => console.log(error))
      },

      getDistance(event) {
        
        axiosInst.get('/rossoftai/runAlgorithm/', {
          params: {
            algthm_type: "distance",
            metric: this.selectedMetric.key,
            obj_1: this.selectedObject1.value,
            obj_2: this.selectedObject2.value,
            lambda: this.lambda,
            name: this.data_name
          }
        }).then(response => {
          
          this.calculatedDistance = response.data

        }).catch(error => console.log(error))
      }
    }
  }
</script>