<template>
  <div class="regression pt-5">
    <h1>Módulo de Bosques Aleatorios</h1>
    <div class="px-7 pt-5 pb-5">
      <FileTable v-model:dataName="this.data_name" />
      <div class="pt-5" v-if="this.data_name">
        <div>
          <h2>Selección de Características</h2>
          <CaracSelec :dataName="this.data_name" v-model:carac="this.selectedCaracteristics" />
        </div>
        <div class="pt-3" v-if="this.selectedCaracteristics.length > 0">
          <h2>Definición de variable a predecir y predictoras</h2>
          <h4><span class="font-semibold">Nota:</span> Al seleccionar una variable de Y, todas las demás serán
            variables predictoras</h4>
          <div class="grid">
            <div class="col-4 right-0 inline">
              <VarSelec :carac="this.selectedCaracteristics" v-model:clase="this.clase" />
            </div>
            <div class="col-4 inline">
              <div class="field">
                <label for="estimators">Número de estimadores: </label>
                <InputNumber :useGrouping="false" :minFractionDigits="0" :maxFractionDigits="0" mode="decimal"
                  v-model="this.estimators" locale="en-US" id="estimators" />
              </div>
              <div class="field">
                <label for="max_depth">Profundidad máxima: </label>
                <InputNumber :useGrouping="false" :minFractionDigits="0" :maxFractionDigits="0" mode="decimal"
                  v-model="this.max_depth" locale="en-US" id="max_depth" />
              </div>
              <div class="field">
                <label for="min_samples_split">Nodos de decisión mínimos: </label>
                <InputNumber :useGrouping="false" :minFractionDigits="0" :maxFractionDigits="0" mode="decimal"
                  v-model="this.min_samples_split" locale="en-US" id="min_samples_split" />
              </div>
              <div class="field">
                <label for="min_samples_leaf">Nodos hoja mínimos: </label>
                <InputNumber :useGrouping="false" :minFractionDigits="0" :maxFractionDigits="0" mode="decimal"
                  v-model="this.min_samples_leaf" locale="en-US" id="min_samples_leaf" />
              </div>
            </div>
            <div class="col-4 left-0 inline pr-3">
              <Button label="Confirmar" @click="confirm" />
            </div>
          </div>
          <div class="pt-5" v-if="this.matrix.length > 0 || this.pronostico.length > 0">
            <Validacion :dataName="this.data_name" :score="this.score" :mae="this.mae" :mse="this.mse" :rmse="this.rmse" :test="this.test" :pronostico="this.pronostico" :importancia="this.importancia" />
            <div class="pt-5">
              <Modelo :dataName="this.data_name" :carac="this.predictoras" />
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
  import InputNumber from 'primevue/inputnumber'


  import {
    defineComponent
  } from '@vue/runtime-core';

  import {
    axiosInst
  } from '../../axios-api'

  export default defineComponent({
    name: 'TreeView',

    components: {
      FileTable,
      CaracSelec,
      VarSelec,
      Button,
      Validacion,
      Modelo,
      InputNumber
    },

    created() {
      this.selectedCaracteristics = []
      this.clase
        this.coef = []
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
        tempdict: null,
        max_depth: null,
        min_samples_split: null,
        min_samples_leaf: null,
        estimators: null,
        mae: null,
        mse: null,
        rmse: null,
        pronostico: [],
        test: [],
        importancia: []
      }
    },

    methods: {
      confirm() {

        var predictoras = new Array()

        this.selectedCaracteristics.forEach(e => {
          if (e != this.clase.name) {
            predictoras[predictoras.length] = e
          }
        })

        this.predictoras = predictoras

        axiosInst.get('/rossoftai/runAlgorithm/', {
          params: {
            name: this.data_name,
            algthm_type: 'tree_regression',
            clase: this.clase.name,
            predictoras: JSON.stringify(this.predictoras),
            max_depth: this.max_depth,
            min_samples_split: this.min_samples_split,
            min_samples_leaf: this.min_samples_leaf,
            estimators: this.estimators,
            estimator_viz: 1
          }
        }).then(res => {

          this.test = res.data[0]
          this.pronostico = res.data[1]
          this.score = res.data[2]['Score']
          this.mae = res.data[2]['MAE']
          this.mse = res.data[2]['MSE']
          this.rmse = res.data[2]['RMSE']
          this.importancia = res.data[3]

        }).catch(err => console.log(err))
      }
    }
  })
</script>