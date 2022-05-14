<template>
  <div class="regression pt-5">
    <h1>Módulo de Regresión Logística</h1>
    <div class="px-7 pt-5 pb-5">
      <FileTable v-model:dataName="this.data_name" />
      <div class="pt-5" v-if="this.data_name">
        <div>
          <h2>Selección de Características</h2>
          <CaracSelec :dataName="this.data_name" v-model:carac="this.selectedCaracteristics" />
        </div>
        <div class="pt-3" v-if="this.selectedCaracteristics.length > 0">
          <h2>Definición de variable de clase y predictoras</h2>
          <h4><span class="font-semibold">Nota:</span> Al seleccionar una variable de clase, todas las demás serán
              variables predictoras</h4>
          <div class="grid">
            <div class="col-6 right-0 inline">
              <VarSelec :carac="this.selectedCaracteristics" v-model:clase="this.clase" />
            </div>
            <div class="col-6 left-0 inline pr-3">
              <Button label="Confirmar" @click="confirm" />
            </div>
          </div>
          <div class="pt-5" v-if="this.coef.length > 0">|
            <Validacion :score="this.score" :intercept="this.intercept" :coef="this.coef" :tempdict="this.tempdict" :matrix="this.matrix"/>
            <div class="pt-5">
              <Modelo :dataName="this.data_name" :intercept="this.intercept" :coef="this.coef" :tempdict="this.tempdict" :carac="this.predictoras" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="js">
  import FileTable from '../../components/FileTable'
  import CaracSelec from '../../components/CaracSelec'
  import VarSelec from '../../components/VarSelec'
  import Button from 'primevue/button'
  import Validacion from '../../components/Validacion'
  import Modelo from '../../components/Modelo'

  import {
    defineComponent
  } from '@vue/runtime-core';

  import {axiosInst} from '../../axios-api'

  export default defineComponent({
    name: 'RegressionView',

    components: {
      FileTable,
      CaracSelec,
      VarSelec,
      Button,
      Validacion,
      Modelo
    },

    created() {
      this.selectedCaracteristics = []
      this.clase,
      this.coef = [],
      this.predictoras = []
    },

    data() {
      return {
        data_name: null,
        selectedCaracteristics: null,
        clase: null,
        score: null,
        intercept: null,
        coef: null,
        matrix: [],
        predictoras: null,
        tempdict: null
      }
    },

    methods: {
      confirm() {

        var predictoras = new Array()

        this.selectedCaracteristics.forEach(e => {
          if ( e != this.clase.name ) {
            predictoras[predictoras.length] = e
          }
        })

        this.predictoras = predictoras
        
        axiosInst.get('/rossoftai/runAlgorithm/', {
          params: {
            name: this.data_name,
            algthm_type: 'regression',
            clase: this.clase.name,
            predictoras: JSON.stringify(predictoras)
          }
        }).then(res => {

          this.score = res.data[0]
          this.intercept = res.data[1]
          this.coef = res.data[2]
          this.matrix = JSON.parse(res.data[3])
          this.tempdict = res.data[4]

          console.log(res.data[4]);

        }).catch(err => console.log(err))
      }
    }
  })
</script>