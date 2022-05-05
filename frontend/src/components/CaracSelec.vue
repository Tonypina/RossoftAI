<template>
    <div class="grid pt-5">
        <div class="col-8">
            <Heatmap :dataName="this.dataName" />
        </div>
        <div class="col-4">
            <h3>Seleccione las características que desea conservar</h3>
            <MultiSelect v-model="selectedCaracteristics" :options="caracteristics" optionLabel="caracteristic"
                placeholder="Seleccione las características" display="chip" />
            <div class="pt-6" v-if="this.selectedCaracteristics.length">
                <Button label="Calcular clusters" @click="sendCaracteristics" />
            </div>
            <div class="pt-6" v-if="!this.selectedCaracteristics.length">
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

        props: ['dataName', 'carac'],
        emits: ['update:carac'],

        methods: {
            sendCaracteristics() {

                var caracteristicsList = new Array()

                this.selectedCaracteristics.forEach(e => {
                    caracteristicsList[caracteristicsList.length] = e.caracteristic
                })

                this.$emit('update:carac', caracteristicsList)
            }
        },

        created() {
            this.dataName
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
                caracteristics: []
            }
        }
    }
</script>

<style lang="scss" scoped>
    .p-multiselect {
        width: 18rem;
    }
</style>