<template>
  <div class="apriori pt-5">
    <h1>Módulo de Clustering Jerárquico</h1>
    <div class="px-7 pt-5 pb-5">
      <h3>Suba la fuente de datos que usará</h3>
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
      <h2>Selección de Características</h2>
      <Button label="Obtener mapa de calor" @click="getHeatmap" />
      <div class="pt-7">
        <highcharts :options="chartOptions"></highcharts>
      </div>
    </div>
  </div>
</template>

<script lang="js">
  import FileUpload from 'primevue/fileupload';
  // import Chart from 'primevue/chart';
  import Highcharts from 'highcharts'
  import heatmapInit from 'highcharts/modules/heatmap.js'
  heatmapInit(Highcharts)


  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Row from 'primevue/row';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';

  import { isProxy, toRaw } from 'vue';


  import {
    axiosInst
  } from '../axios-api'
  import {
    defineComponent
  } from '@vue/runtime-core';

  function getPointCategoryName(point, dimension) {
    var series = point.series,
      isY = dimension === 'y',
      axis = series[isY ? 'yAxis' : 'xAxis'];
    return axis.categories[point[isY ? 'y' : 'x']];
  }

  export default defineComponent({
    name: 'HClustView',

    components: {
      FileUpload,
      chart: Highcharts,
      DataTable,
      Column,
      Row,
      InputText,
      Button
    },
    data() {
      return {
        data_name: null,
        correlational_data: null,
        file: '',
        fileLimit: 1,
        datos: null,
        columns_datos: null,
        chartOptions: {
          chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 80,
            plotBorderWidth: 1
          },


          title: {
            text: 'Mapa de calor correlacional'
          },

          xAxis: {
            categories: null
          },

          yAxis: {
            categories: null,
            title: null,
            // reversed: true
          },

          accessibility: {
            point: {
              descriptionFormatter: function (point) {
                var ix = point.index + 1,
                  xName = getPointCategoryName(point, 'x'),
                  yName = getPointCategoryName(point, 'y'),
                  val = point.value;
                return ix + '. ' + xName + ' sales ' + yName + ', ' + val + '.';
              }
            }
          },

          colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[0]
          },

          legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 280
          },

          tooltip: {
            formatter: function () {
              return '<b>' + getPointCategoryName(this.point, 'x') + '</b> sold <br><b>' +
                this.point.value + '</b> items on <br><b>' + getPointCategoryName(this.point, 'y') + '</b>';
            }
          },

          series: [{
            // name: 'Sales per employee',
            borderWidth: 1,
            data: [],
            dataLabels: {
              enabled: true,
              color: '#000000'
            }
          }],

          responsive: {
            rules: [{
              condition: {
                maxWidth: 500
              },
              chartOptions: {
                yAxis: {
                  labels: {
                    formatter: function () {
                      return this.value.charAt(0);
                    }
                  }
                }
              }
            }]
          }
        }
      }
    },
    created() {
      this.columns_datos = [],
      this.datos = []
      // this.chartOptions.series.data = new Array()
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
            })
          .then(response => {
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
              }
              this.datos = dataList

            }).catch(function (error) {
              console.log(error)
            })
          })
          .catch(function (error) {
            console.log(error)
          });
      },

      getHeatmap(event) {
        axiosInst.get('/rossoftai/runAlgorithm/', {
          params: {
            algthm_type: "selec",
            name: this.data_name
          }
        }).then(response => {
          
          var headersList = Object.keys(response.data[0])

          this.chartOptions.xAxis.categories = headersList
          this.chartOptions.yAxis.categories = headersList

          console.log(typeof this.chartOptions.series.data)
          console.log(response.data[1])

          let arreglo = new Array()

          for (let i = 0; i < response.data[1].length; i++) {
            for (let j = 0; j < response.data[1][i].length; j++) {
              arreglo[arreglo.length] = [
                j,
                i,
                response.data[1][i][j]
              ]
            }
          }
          console.log(arreglo)
          this.chartOptions.series[0].data = arreglo
          console.log(this.chartOptions.series.data)
        })
      }
    }
  });
</script>