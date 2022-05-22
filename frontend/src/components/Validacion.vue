<template>
    <div class="pt-5">
        <h2>Validación del modelo</h2>
        <div class="grid">
            <div class="col-3">
                <h3>Parámetros útiles</h3>
                <h4>Score: {{ this.score }}</h4>
                <div v-if="this.matrix">
                    <h4>Tasa de Error: {{ this.error }}</h4>
                    <h4>Precisión: {{ this.precision }}</h4>
                    <h4>Sensibilidad: {{ this.sensibilidad }}</h4>
                    <h4>Especificidad: {{ this.especificidad }}</h4>
                    <div v-if="this.intercept">
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
                </div>
                <div v-else-if="!this.matrix">
                    <h4>MAE: {{ this.mae }}</h4>
                    <h4>MSE: {{ this.mse }}</h4>
                    <h4>RMSE: {{ this.rmse }}</h4>
                </div>
            </div>
            <div class="col-9" v-if="this.matrix">
                <div class="grid">
                    <div class="col-5 col-offset-1">
                        <Chart type="polarArea" :data="chartData" :options="chartOptions" />
                    </div>
                    <div class="col-5 col-offset-1">
                        <h3>Matriz de Clasificación</h3>
                        <DataTable :value="clasification_matrix" responsiveLayout="scroll">
                            <Column v-for="col of matrix_cols" :field="col.field" :header="col.header" :key="col.field">
                            </Column>
                        </DataTable>
                    </div>
                </div>
            </div>
            <div class="col-9" v-else-if="!this.matrix">
                <div class="grid">
                    <div class="col-11 col-offset-1">
                        <Chart type="line" :data="lineChartData" :options="basicOptions" />
                    </div>
                </div>
            </div>
        </div>
        <div v-if="!this.intercept">
            <div class="pt-5">
                <h2>Diagrama del árbol</h2>
                <div class="w-full overflow-scroll">
                    <img class="" :src="this.tree" alt="Diagrama de arbol">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import DataTable from 'primevue/datatable'
    import Column from 'primevue/column'
    import Row from 'primevue/row'
    import Chart from 'primevue/chart'

    import Functions from '../functions'
    import {
        axiosInst
    } from '../axios-api'

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

        props: ['dataName', 'score', 'intercept', 'coef', 'tempdict', 'matrix', 'mae', 'mse', 'rmse', 'test',
            'pronostico', 'importancia'
        ],

        components: {
            DataTable,
            Column,
            Row,
            Chart
        },

        created() {
            this.clasification_matrix = []
            this.matrix_cols = []
        },

        mounted() {

            if (!this.intercept) {
                axiosInst.get('/rossoftai/runAlgorithm/', {
                    params: {
                        name: this.dataName,
                        algthm_type: 'get_tree'
                    },

                    headers: {
                        'content-type': 'image/png',
                    },

                    responseType: 'blob'

                }).then(res => {

                    const urlCreator = window.URL || window.webkitURL

                    this.tree = urlCreator.createObjectURL(res.data)
                }).catch(err => console.log(err))
            }

            if (this.matrix) {

                var headersList = Object.keys(this.matrix[0])

                for (let i = 0; i < headersList.length; i++) {
                    this.tempdict ?
                        this.matrix_cols[i] = {
                            field: headersList[i].toString(),
                            header: this.tempdict[i]
                        } :
                        this.matrix_cols[i] = {
                            field: headersList[i].toString(),
                            header: headersList[i]
                        }
                }
                this.clasification_matrix = this.matrix

                for (let i = 0; i < this.matrix.length; i++) {
                    for (let j = 0; j < headersList.length; j++) {
                        this.tempdict ?
                            this.chartData.labels[this.chartData.labels.length] = this.tempdict[i] + this.tempdict[j] :
                            this.chartData.labels[this.chartData.labels.length] = headersList[i] + headersList[j]
                        
                        this.chartData.datasets[0].backgroundColor[this.chartData.datasets[0].backgroundColor.length] = ColorCode()

                        this.tempdict ?
                            this.chartData.datasets[0].data[this.chartData.datasets[0].data.length] = this.matrix[i][j] :
                            this.chartData.datasets[0].data[this.chartData.datasets[0].data.length] = this.matrix[i][headersList[j]]
                    }
                }

                var matrix_params = this.chartData.datasets[0].data

                var sum = matrix_params[0] + matrix_params[3] + matrix_params[1] + matrix_params[2]

                this.error = new Functions().round((matrix_params[1] + matrix_params[2]) / sum)
                this.precision = new Functions().round((matrix_params[0]) / (matrix_params[0] + matrix_params[2]))
                this.sensibilidad = new Functions().round((matrix_params[0]) / (matrix_params[0] + matrix_params[1]))
                this.especificidad = new Functions().round((matrix_params[3]) / (matrix_params[2] + matrix_params[3]))

            } else {

                for (let i = 0; i < this.pronostico.length; i++) {
                    this.lineChartData.labels[i] = i

                    this.lineChartData.datasets[0].data[i] = this.test[i][0]
                    this.lineChartData.datasets[1].data[i] = this.pronostico[i]
                }

                console.log(this.test)
            }
        },

        data() {
            return {
                clasification_matrix: null,
                matrix_cols: null,
                matrix_params: null,
                error: null,
                precision: null,
                sensibilidad: null,
                especificidad: null,
                tree: null,

                chartData: {
                    datasets: [{
                        data: [],
                        backgroundColor: [],
                        label: 'Gráfica de clasificación'
                    }],
                    labels: []
                },

                lineChartData: {
                    labels: [],
                    datasets: [{
                            label: 'Test',
                            data: [],
                            fill: false,
                            borderColor: '#F56800',
                            tension: 0
                        },
                        {
                            label: 'Pronostico',
                            data: [],
                            fill: false,
                            borderColor: '#000000',
                            tension: 0
                        }
                    ]
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
                },

                basicOptions: {
                    plugins: {
                        legend: {
                            labels: {
                                color: '#495057'
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: {
                                color: '#495057'
                            },
                            grid: {
                                color: '#ebedef'
                            }
                        },
                        y: {
                            ticks: {
                                color: '#495057'
                            },
                            grid: {
                                color: '#ebedef'
                            }
                        }
                    }
                },
            }
        }
    }
</script>