<template>
  <div class="p-clust pt-5">
    <h1>Módulo de Clustering Particional</h1>
    <div class="px-7 pt-5 pb-5">
      <h3>Suba la fuente de datos que usará</h3>
      <FileUpload name="file" :customUpload="true" @uploader="uploader" chooseLabel="Elegir" uploadLabel="Subir"
        cancelLabel="Cancelar">
        <template #empty>
          <p>Suelte su archivo aquí</p>
        </template>
      </FileUpload>
    </div>
  </div>
</template>

<script lang="js">
  import FileUpload from 'primevue/fileupload';
  import Chart from 'primevue/chart';

  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Row from 'primevue/row';
  import InputText from 'primevue/inputtext';
  import Button from 'primevue/button';
  import MultiSelect from 'primevue/multiselect';

  import Functions from '../functions.js'

  import {
    axiosInst
  } from '../axios-api'

  function getPointCategoryName(point, dimension) {
    var series = point.series,
      isY = dimension === 'y',
      axis = series[isY ? 'yAxis' : 'xAxis'];
    return axis.categories[point[isY ? 'y' : 'x']];
  }

  function round(num) {
    var m = Number((Math.abs(num) * 100).toPrecision(15));
    return Math.round(m) / 100 * Math.sign(num);
  }

  export default {
    name: 'PClustView',

    data() {
      return {
        data_name: null,
        datos: [],
        columns_datos: []
      }
    },

    components: {
      FileUpload,
      chart: Highcharts,
      DataTable,
      Column,
      Row,
      InputText,
      Button,
      MultiSelect
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
      }
    }
  }
</script>
