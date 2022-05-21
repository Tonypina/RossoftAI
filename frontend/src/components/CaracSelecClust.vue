<template>
    <div class="grid pt-5">
        <div class="col-8">
            <Heatmap :dataName="this.dataName" />
        </div>
        <div class="col-4">
            <h3>Seleccione las características que desea conservar</h3>
            <MultiSelect v-model="selectedCaracteristics" :options="caracteristics" optionLabel="caracteristic"
                placeholder="Seleccione las características" display="chip" />
            <div v-if="this.clustType != 'kmeans'">
                <div class="pt-4">
                    <h3>Seleccione una métrica</h3>
                    <Dropdown v-model="selectedMetric" :options="metrics" optionLabel="name"
                        placeholder="Selecciona una métrica" />
                </div>
                <div class="pt-6">
                    <Button label="Graficar clusters" @click="sendCaracteristics"
                        :disabled="!(this.selectedMetric && this.selectedCaracteristics.length)" />
                </div>
            </div>
            <div v-else-if="this.clustType == 'kmeans'">
                <div class="pt-6">
                    <Button label="Calcular clusters" @click="sendCaracteristics"
                        :disabled="!(this.selectedCaracteristics.length)" />
                </div>
            </div>
        </div>
        <div class="grid" v-if="this.dendrogram">
            <div class="col-4">
                <h3>Basado en el diagrama, indique el número de clusters que desea</h3>
                <InputNumber v-model="this.nClust_local" mode="decimal" :minFractionDigits="0" :maxFractionDigits="0" />
                <div class="pt-6">
                    <Button label="Calcular clusters" @click="accept" :disabled="!(this.nClust_local > 0)" />
                </div>
            </div>
            <div class="col-8">
                <h3>Dendrograma obtenido</h3>
                <div class="w-full">
                    <img class="w-full" :src="this.dendrogram" alt="Dendrograma">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import Heatmap from './Heatmap.vue'
    import MultiSelect from 'primevue/multiselect'
    import Button from 'primevue/button'
    import InputNumber from 'primevue/inputnumber'
    import Dropdown from 'primevue/dropdown'

    import {
        axiosInst
    } from '../axios-api'

    export default {
        name: 'CaracSelecClust',

        components: {
            Heatmap,
            MultiSelect,
            Button,
            InputNumber,
            Dropdown
        },

        props: ['dataName', 'dataClust', 'clustType', 'sse', 'elbow', 'carac', 'centroides'],
        emits: ['update:centroides', 'update:dataClust', 'update:sse', 'update:elbow', 'update:carac'],

        methods: {

            accept() {

                var caracteristicsList = new Array()

                this.selectedCaracteristics.forEach(e => {
                    caracteristicsList[caracteristicsList.length] = e.caracteristic
                })

                axiosInst.get('/rossoftai/runAlgorithm/', {
                    params: {
                        algthm_type: this.clustType,
                        name: this.dataName,
                        nClust: this.nClust_local,
                        carac: JSON.stringify(caracteristicsList)
                    }
                }).then(response => {
                    this.centroides_local = response.data[1]
                    this.dataClust_local = response.data[0]

                    this.$emit('update:centroides', JSON.parse(this.centroides_local))
                    this.$emit('update:dataClust', JSON.parse(this.dataClust_local))

                }).catch(error => console.log(error))
            },

            sendCaracteristics() {

                var caracteristicsList = new Array()

                this.selectedCaracteristics.forEach(e => {
                    caracteristicsList[caracteristicsList.length] = e.caracteristic
                })

                if (this.clustType == 'kmeans') {

                    axiosInst.get('/rossoftai/runAlgorithm/', {
                        params: {
                            algthm_type: this.clustType,
                            name: this.dataName,
                            carac: JSON.stringify(caracteristicsList)
                        }
                    }).then(response => {
                        this.sse_local = response.data[0]
                        this.elbow_local = response.data[1]

                        this.$emit('update:sse', this.sse_local)
                        this.$emit('update:elbow', this.elbow_local)
                        this.$emit('update:carac', caracteristicsList)


                    }).catch(error => console.log(error))

                } else {

                    axiosInst.get('/rossoftai/runAlgorithm/', {
                        params: {
                            algthm_type: 'get_dendrogram',
                            name: this.dataName,
                            metric: this.selectedMetric.key,
                            carac: JSON.stringify(caracteristicsList)
                        },

                        headers: {
                            'content-type': 'image/png',
                        },

                        responseType: 'blob'
                    }).then(response => {

                        const urlCreator = window.URL || window.webkitURL

                        this.dendrogram = urlCreator.createObjectURL(response.data)

                    }).catch(error => console.log(error))
                }
            }
        },

        created() {
            this.dataName,
                this.clustType,
                this.centroides_local = [],
                this.dataClust_local = []
            this.sse_local = [],
                this.elbow_local
            this.nClust_local
        },

        mounted() {

            axiosInst.get('/rossoftai/runAlgorithm/', {
                params: {
                    algthm_type: "selec",
                    name: this.dataName
                }
            }).then(response => {
                var headersList = Object.keys(response.data[0])

                headersList.forEach(e => {
                    this.caracteristics[this.caracteristics.length] = {
                        caracteristic: e
                    }
                })

            }).catch(err => console.log(err))
        },

        data() {
            return {
                selectedCaracteristics: [],
                selectedMetric: null,
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
                dendrogram: null,
                caracteristics: [],
                nClust: null,
                centroides_local: null,
                dataClust_local: null,
                sse_local: null,
                elbow_local: null,
                nClust_local: null
            }
        }
    }
</script>

<style lang="scss" scoped>
    .p-multiselect {
        width: 18rem;
    }
</style>