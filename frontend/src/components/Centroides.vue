<template>
    <div>
        <DataTable :value="centroides" responsiveLayout="scroll" :scrollable="true" scrollHeight="400px">
            <Column v-for="col of columns_centroides" :field="col.field" :header="col.header" :key="col.field"></Column>
        </DataTable>
        <div class="pt-6">
            <highcharts :options="chartOptions"></highcharts>
        </div>
    </div>
</template>

<script>
    import DataTable from 'primevue/datatable'
    import Column from 'primevue/column'
    import Row from 'primevue/row'

    import Highcharts from 'highcharts'

    function round(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }

    export default {
        name: 'Centroides',

        components: {
            DataTable,
            Column,
            Row,
            chart: Highcharts
        },

        props: {
            centroides: Array,
            dataClust: Array
        },


        created() {
            this.centroides
            this.dataClust
            this.columns_centroides = []
        },

        mounted() {

            var headersList = Object.keys(this.centroides[0])

            var centroides_local = this.centroides

            centroides_local.forEach(e => {
                headersList.forEach(i => {
                    e[i] = round(e[i])
                })
            })

            for (let i = 0; i < headersList.length; i++) {
                this.columns_centroides[i] = {
                    field: headersList[i],
                    header: headersList[i]
                }
            }

            var dataClust_local = this.dataClust
            var data_aux = new Array()

            dataClust_local.forEach(e => {
                data_aux[data_aux.length] = {
                    0: e['cluster'],
                    1: [e[headersList[0]], e[headersList[1]]]
                }
            })

            for (let i = 0; i < centroides_local.length; i++) {
                
                var data_aux_2 = new Array()
                data_aux.forEach(e => {
                    if (e[0] == i) {
                        data_aux_2[data_aux_2.length] = e[1]
                    }
                })

                this.chartOptions.series[i] = {
                    name: i,
                    data: data_aux_2
                }
            }

            console.log(data_aux_2)
        },

        data() {
            return {
                columns_centroides: null,

                chartOptions: {

                    chart: {
                        type: 'scatter',
                        zoomType: 'xy'
                    },
                    title: {
                        text: 'Distribución de los datos en los clusters'
                    },
                    xAxis: {
                        startOnTick: true,
                        endOnTick: true,
                        showLastLabel: true
                    },
                    yAxis: {},
                    legend: {
                        layout: 'vertical',
                        align: 'left',
                        verticalAlign: 'top',
                        x: 100,
                        y: 70,
                        floating: true,
                        backgroundColor: Highcharts.defaultOptions.chart.backgroundColor,
                        borderWidth: 1
                    },
                    plotOptions: {
                        scatter: {
                            marker: {
                                radius: 5,
                                states: {
                                    hover: {
                                        enabled: true,
                                        lineColor: 'rgb(100,100,100)'
                                    }
                                }
                            },
                            states: {
                                hover: {
                                    marker: {
                                        enabled: false
                                    }
                                }
                            },
                            tooltip: {
                                headerFormat: '<b>{series.name}</b><br>',
                                pointFormat: '{point.x}, {point.y}'
                            }
                        }
                    },
                    series: []
                }

            }
        },

    }
</script>