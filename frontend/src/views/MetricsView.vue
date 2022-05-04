<template>
  <div class="metrics pt-5 pb-5 px-8">
    <h1>Módulo de <span>Métricas</span></h1>

    <div class="grid">
      <div class="col-7">
        <h3>Ingrese la fuente de datos</h3>
        <FileUpload name="file" :customUpload="true" @uploader="uploader" chooseLabel="Elegir" uploadLabel="Subir"
          cancelLabel="Cancelar">
          <template #empty>
            <p>Suelte su archivo aquí</p>
          </template>
        </FileUpload>
      </div>
      <div class="col-5">
        <h3>El archivo que envió se llama:</h3>
        <h3>{{ data_name }}</h3>
      </div>
    </div>
  </div>
</template>

<script>
  import FileUpload from 'primevue/fileupload';
  import Chart from 'primevue/chart';
  import DataTable from 'primevue/datatable';
  import Column from 'primevue/column';
  import Row from 'primevue/row';
  
  import { axiosInst } from '../axios-api';

  export default {
    name: 'MetricsView',

    components: {
      FileUpload,
      Chart,
      DataTable,
      Column,
      Row
    },

    data() {
      return {
        data_name: ''
      }
    },

    created() {
    
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
        ).then(response => this.data_name = response.data)
        .catch(error => console.log(error))
      }
    }
  }
</script>