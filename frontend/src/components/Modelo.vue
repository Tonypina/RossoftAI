<template>
    <div class="pt-5">
        <h2>Modelo de clasificación</h2>
        <h3>Introduzca los valores del objeto a clasificar</h3>
        <div class="p-fluid grid pt-3">
            <div class="col-6">
                <div v-for="c of this.carac_1" :key="c" class="flex justify-content-center">
                    <div class="field w-6 mb-0">
                        <h4 class="text-left">{{ c }}: </h4>
                        <InputNumber :useGrouping="false" :minFractionDigits="1" :maxFractionDigits="5" mode="decimal" :id="c" v-model="this.values[c]" locale="en-US"/>
                    </div>
                </div>
            </div>
            <div class="col-6">
                <div v-for="c of this.carac_2" :key="c" class="flex justify-content-center">
                    <div class="field w-6 mb-0">
                        <h4 class="text-left">{{ c }}: </h4>
                        <InputNumber :useGrouping="false" :minFractionDigits="1" :maxFractionDigits="5" mode="decimal" :id="c" v-model="this.values[c]" locale="en-US"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-5">
            <Button label="Calcular" @click="calcular" />
        </div>
        <h2>Resultado: {{ this.result }}</h2>
    </div>
</template>

<script>
    import InputNumber from 'primevue/inputnumber'
    import Button from 'primevue/button'
    import { axiosInst } from '../axios-api'

    export default {
        name: 'Modelo',

        props: ['dataName', 'intercept', 'coef', 'tempdict', 'carac', 'y'],

        components: {
            InputNumber,
            Button
        },

        mounted() {
            this.carac_1 = []
            this.carac_2 = []
            this.values = {}

            var half = parseInt(this.carac.length / 2)

            for (let i = 0; i < half; i++) {
                this.carac_1[this.carac_1.length] = this.carac[i]
            }

            for (let i = half; i < this.carac.length; i++) {
                this.carac_2[this.carac_2.length] = this.carac[i]
            }

            this.carac.forEach(element => {
                this.values[element] = null
            })
        },

        data() {
            return {
                carac_1: null,
                carac_2: null,
                result: null,
                values: null
            }
        },

        methods: {
            calcular() {

                var arrayValues = new Array()
                this.carac.forEach(element => {
                    arrayValues[arrayValues.length] = this.values[element]
                })

                axiosInst.get('/rossoftai/runAlgorithm/', {
                    params: {
                        name: this.dataName,
                        algthm_type: 'predict',
                        values: JSON.stringify(arrayValues),
                        predictoras: JSON.stringify(this.carac)
                    }
                }).then(res => {

                    this.tempdict ?
                        this.result = this.tempdict[res.data]:
                        this.result = res.data[0]

                }).catch(err => console.log(err))
            }
        }
    }
</script>