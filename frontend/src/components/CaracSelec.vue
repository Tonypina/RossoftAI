<template>
    <div class="grid pt-5">
        <div class="col-8">
            <Heatmap :dataName="this.dataName" />
        </div>
        <div class="col-4">
            <h3>Seleccione las características que desea conservar</h3>
            <MultiSelect v-model="selectedCaracteristics" :options="caracteristics" optionLabel="caracteristic"
                placeholder="Seleccione las características" display="chip" />
            <div class="pt-4">
                <h3>Número de clusters</h3>
                <InputText v-model="this.nClust" />
            </div>
            <div class="pt-6" v-if="this.nClust && this.nClust != 0 && this.selectedCaracteristics.length">
                <Button label="Calcular clusters" @click="sendCaracteristics" />
            </div>
            <div class="pt-6" v-if="!this.nClust || this.nClust == 0 || !this.selectedCaracteristics.length">
                <Button label="Calcular clusters" disabled="disabled" />
            </div>
        </div>
    </div>
</template>

<script>
    import Heatmap from './Heatmap.vue'
    import MultiSelect from 'primevue/multiselect'
    import Button from 'primevue/button'
    import InputText from 'primevue/inputtext'

    import {
        axiosInst
    } from '../axios-api'

    export default {
        name: 'CaracSelec',

        components: {
            Heatmap,
            MultiSelect,
            Button,
            InputText
        },

        props: ['dataName', 'centroides', 'dataClust'],
        emits: ['update:centroides', 'update:dataClust'],

        methods: {
            sendCaracteristics() {

                var caracteristicsList = new Array()

                this.selectedCaracteristics.forEach(e => {
                    caracteristicsList[caracteristicsList.length] = e.caracteristic
                });

                axiosInst.get('/rossoftai/runAlgorithm/', {
                    params: {
                        algthm_type: "hclust",
                        name: this.dataName,
                        nClust: this.nClust,
                        carac: JSON.stringify(caracteristicsList)
                    }
                }).then(response => {

                    this.centroides_local = response.data[1]
                    this.dataClust_local = response.data[0]

                    this.$emit('update:centroides', JSON.parse(this.centroides_local))
                    this.$emit('update:dataClust', JSON.parse(this.dataClust_local))

                }).catch(error => console.log(error))
            }
        },

        created() {
            this.dataName,
            this.centroides_local = [],
            this.dataClust_local = []
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

            })
        },

        data() {
            return {
                selectedCaracteristics: [],
                caracteristics: [],
                nClust: null,
                centroides_local: null,
                dataClust_local: null
            }
        }
    }
</script>

<style lang="scss" scoped>
    .p-multiselect {
        width: 18rem;
    }
</style>