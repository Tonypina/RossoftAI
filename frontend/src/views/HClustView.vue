<template>
  <div class="apriori pt-5">
    <h2>Ingrese la fuente de datos con la que trabajará</h2>
    <div class="px-7 pt-5 pb-5">
      <FileUpload name="file" :customUpload="true" @uploader="uploader" chooseLabel="Elegir" uploadLabel="Subir"
        cancelLabel="Cancelar">
        <template #empty>
          <p>Suelte su archivo aquí</p>
        </template>
      </FileUpload>
    </div>
    <div class="">
      <h2>Exploración de datos</h2>
    </div>
  </div>
</template>

<script lang="js">
  import FileUpload from 'primevue/fileupload';
  import {
    axiosInst
  } from '../axios-api'
  import {
    defineComponent
  } from '@vue/runtime-core';

  function file_extension(filename) {
    return (/[.]/.exec(filename)) ? /[^.]+$/.exec(filename)[0] : undefined;
  }

  export default defineComponent({
    name: 'HClustView',

    components: {
      FileUpload
    },
    data() {
      return {
        file: '',
        fileLimit: 1
      }
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
          .then(function (response) {
            console.log(response);

            axiosInst.get('/rossoftai/runAlgorithm/',{
              params: {
                algthm_type: "apriori",
                name: response.data,
                support: 0.01,
                confidence: 0.3,
                lift: 2
              }
            }).then(function (response) {
              console.log(response)
            }).catch(function (error) {
              console.log(error)
            })
          })
          .catch(function (error) {
            console.log(error)
          });
      }
    }
  });
</script>