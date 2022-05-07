<template>
    <div class="pt-5">
        <div class="grid">
            <div class="col-3">
                <h3>Parámetros útiles</h3>
                <h4>Score: {{ this.score }}</h4>
                <h4>Intercepto: {{ this.intercept[0] }}</h4>
                <h4>Coeficientes: </h4>
                <ul>
                    <div v-for="e of this.coef[0]" :key="e">
                        <li>
                            <h5 class="inline">{{ e }}</h5>
                        </li>
                    </div>
                </ul>
            </div>
            <div class="col-4 col-offset-1">
                <Chart type="polarArea" :data="chartData" :options="chartOptions" />
            </div>
            <div class="col-3 col-offset-1">
                <h3>Matriz de Clasificación</h3>
                <DataTable :value="clasification_matrix" responsiveLayout="scroll">
                    <Column v-for="col of matrix_cols" :field="col.field" :name="col.name" :key="col.field"></Column>
                </DataTable>
            </div>
        </div>
    </div>
</template>

<script>
    import DataTable from 'primevue/datatable'
    import Column from 'primevue/column'
    import Row from 'primevue/row'
    import Chart from 'primevue/chart'

    function ColorCode() {
        var makingColorCode = '0123456789ABCDEF';
        var finalCode = '#';
        for (var counter = 0; counter < 6; counter++) {
            finalCode = finalCode + makingColorCode[Math.floor(Math.random() * 16)];
        }
        return finalCode;
    }

    export default {
        name: 'Validacion',

        props: ['score', 'intercept', 'coef', 'matrix'],

        components: {
            DataTable,
            Column,
            Row,
            Chart
        },

        created() {
            this.clasification_matrix = [],
                this.matrix_cols = []
        },

        mounted() {

            // console.log(this.matrix);

            var headersList = Object.keys(this.matrix[0])
            var valuesList = new Array()

            for (let i = 0; i < headersList.length; i++) {
                this.matrix_cols[i] = {
                    field: headersList[i].toString(),
                    header: headersList[i].toString()
                }
            }
            this.clasification_matrix = this.matrix

            for (let i = 0; i < this.matrix.length; i++) {
                for (let j = 0; j < headersList.length; j++) {
                    this.chartData.labels[this.chartData.labels.length] = i.toString() + j.toString()
                    this.chartData.datasets[0].backgroundColor[this.chartData.datasets[0].backgroundColor.length] =
                        ColorCode()
                    this.chartData.datasets[0].data[this.chartData.datasets[0].data.length] = this.matrix[i][j]
                }
            }

        },

        data() {
            return {
                clasification_matrix: null,
                matrix_cols: null,

                chartData: {
                    datasets: [{
                        data: [],
                        backgroundColor: [],
                        label: 'Gráfica de clasificación'
                    }],
                    labels: []
                },

                chartOptions: {
                    plugins: {
                        legend: {
                            labels: {
                                color: '#495057'
                            }
                        }
                    },
                    scales: {
                        r: {
                            grid: {
                                color: '#ebedef'
                            }
                        }
                    }
                }
            }
        }
    }
</script>