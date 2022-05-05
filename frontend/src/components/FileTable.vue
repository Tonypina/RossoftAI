<template>
    <div>
        <h3>Suba la fuente de datos que usará</h3>
        <FileUpload name="file" :customUpload="true" @uploader="uploader" chooseLabel="Elegir" uploadLabel="Subir"
            cancelLabel="Cancelar">
            <template #empty>
                <p>Suelte su archivo aquí</p>
            </template>
        </FileUpload>
        <h2>Datos</h2>
        <DataTable :value="datos" responsiveLayout="scroll" :scrollable="true" scrollHeight="400px">
            <Column v-for="col of columns_datos" :field="col.field" :header="col.header" :key="col.field"></Column>
        </DataTable>
        <h2>Relación</h2>
        <h3>Selecciona dos características</h3>
        <div class="pt-2 pb-4">
            <div class="pr-4 inline">
                <Dropdown v-model="selectedCar1" :options="headersList" optionLabel="name"
                    placeholder="Selecciona una característica" />
            </div>
            <div class="pr-4 inline">
                <Dropdown v-model="selectedCar2" :options="headersList" optionLabel="name"
                    placeholder="Selecciona una característica" />
            </div>
            <Button label="Graficar" @click="plot" />
        </div>
        <Chart type="line" :data="chartData" />
    </div>
</template>
<script>
    import DataTable from 'primevue/datatable';
    import Column from 'primevue/column';
    import Row from 'primevue/row';
    import FileUpload from 'primevue/fileupload'
    import Chart from 'primevue/chart'
    import Dropdown from 'primevue/dropdown';
    import Button from 'primevue/button'

    import {
        axiosInst
    } from '../axios-api'

    export default {
        name: 'FileTable',

        props: ['dataName'],
        emits: ['update:dataName'],

        mounted() {
            this.data_name,
                this.datos = [],
                this.columns_datos = [],
                this.headersList = []
        },

        data() {
            return {
                file: '',
                data_name: null,
                datos: null,
                columns_datos: null,
                selectedCar1: null,
                selectedCar2: null,
                headersList: null,

                chartData: {
                    labels: [],
                    datasets: [{
                        label: 'Datos',
                        data: [],
                        fill: false,
                        borderColor: '#42A5F5',
                        tension: 0
                    }]
                }
            }
        },

        components: {
            DataTable,
            FileUpload,
            Column,
            Row,
            Dropdown,
            Chart,
            Button
        },

        methods: {
            plot() {

                var labels = new Array()
                var dataset = new Array()
                this.datos.forEach(element => {
                    labels[labels.length] = element[this.selectedCar1.name]
                    dataset[dataset.length] = element[this.selectedCar2.name]
                })

                this.chartData.labels = labels
                this.chartData.datasets[0].data = dataset

            },

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
                    )
                    .then(response => {
                        this.data_name = response.data

                        this.$emit('update:dataName', this.data_name)

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

                            headersList.forEach(e => {
                                this.headersList[this.headersList.length] = {
                                    name: e
                                }
                            })

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