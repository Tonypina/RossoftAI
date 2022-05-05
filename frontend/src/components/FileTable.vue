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
    </div>
</template>
<script>
    import DataTable from 'primevue/datatable';
    import Column from 'primevue/column';
    import Row from 'primevue/row';
    import FileUpload from 'primevue/fileupload'

    import { axiosInst } from '../axios-api'

    export default {
        name: 'FileTable',

        props: ['dataName'],
        emits: ['update:dataName'],

        mounted() {
            this.data_name,
            this.datos = [],
            this.columns_datos = []
        },

        data() {
            return {
                file: '',
                data_name: null,
                datos: null,
                columns_datos: null
            }
        },

        components: {
            DataTable,
            FileUpload,
            Column,
            Row,
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