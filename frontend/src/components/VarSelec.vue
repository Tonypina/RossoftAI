<template>
    <div>
        <div class="">
            <h3 class="inline pr-3">Seleccione la variable clase: </h3>
            <div class="inline pr-3">
                <Dropdown v-model="selectedVariable" :options="variables" optionLabel="name"
                    placeholder="Selecciona una variable" @change="change"/>
            </div>
        </div>
    </div>
</template>
<script>
    import Dropdown from 'primevue/dropdown'
    import Button from 'primevue/button'

    import {
        axiosInst
    } from '../axios-api'

    export default {
        name: 'VarSelec',

        props: ['carac', 'clase'],
        emits: ['update:clase'],

        components: {
            Dropdown,
            Button
        },

        mounted() {

            this.carac.forEach(e => {
                this.variables[this.variables.length] = {
                    name: e
                }
            })
        },

        data() {
            return {
                selectedVariable: null,
                variables: []
            }
        },

        methods: {
            change() {

                this.$emit('update:clase', this.selectedVariable)
            }
        }
    }
</script>