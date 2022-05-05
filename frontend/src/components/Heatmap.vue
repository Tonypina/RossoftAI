<template>
    <highcharts :options="chartOptions"></highcharts>
</template>

<script>
    import { defineComponent } from 'vue'
    import Highcharts from 'highcharts'
    import heatmapInit from 'highcharts/modules/heatmap.js'
    heatmapInit(Highcharts)

    import { axiosInst } from '../axios-api'
    
    function getPointCategoryName(point, dimension) {
        var series = point.series,
        isY = dimension === 'y',
        axis = series[isY ? 'yAxis' : 'xAxis'];
        return axis.categories[point[isY ? 'y' : 'x']];
    }

    function round(num) {
        var m = Number((Math.abs(num) * 100).toPrecision(15));
        return Math.round(m) / 100 * Math.sign(num);
    }

    export default defineComponent({
        name: 'Heatmap',

        components: {
            chart: Highcharts,
        },

        props: {
            dataName: String
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

                this.chartOptions.xAxis.categories = headersList
                this.chartOptions.yAxis.categories = headersList

                let arreglo = new Array()

                for (let i = 0; i < response.data[1].length; i++) {
                    for (let j = 0; j < response.data[1][i].length; j++) {
                        arreglo[arreglo.length] = [
                            j,
                            i,
                            round(response.data[1][i][j])
                        ]
                    }
                }
                this.chartOptions.series[0].data = arreglo
            })

        },

        data() {
            return {
                correlational_data: null,
                chartOptions: {
                    chart: {
                        type: 'heatmap',
                        marginTop: 40,
                        marginBottom: 80,
                        plotBorderWidth: 1
                    },


                    title: {
                        text: 'Mapa de calor correlacional'
                    },

                    xAxis: {
                        categories: null
                    },

                    yAxis: {
                        categories: null,
                        title: null,
                    },

                    accessibility: {
                        point: {
                            descriptionFormatter: function (point) {
                                var ix = point.index + 1,
                                xName = getPointCategoryName(point, 'x'),
                                yName = getPointCategoryName(point, 'y'),
                                val = point.value;
                                return ix + '. ' + xName + ' sales ' + yName + ', ' + val + '.';
                            }
                        }
                    },

                    colorAxis: {
                        min: 0,
                        minColor: '#FFFFFF',
                        maxColor: Highcharts.getOptions().colors[0]
                    },

                    legend: {
                        align: 'right',
                        layout: 'vertical',
                        margin: 0,
                        verticalAlign: 'top',
                        y: 25,
                        symbolHeight: 280
                    },

                    tooltip: {
                        formatter: function () {
                        return '<b>' + getPointCategoryName(this.point, 'x') +
                            this.point.value + '</b> items en <br><b>' + getPointCategoryName(this.point, 'y') + '</b>';
                        }
                    },

                    series: [{
                        borderWidth: 1,
                        data: [],
                        dataLabels: {
                            enabled: true,
                            color: '#000000'
                        }
                    }],

                    responsive: {
                        rules: [{
                            condition: {
                                maxWidth: 500
                            },
                            chartOptions: {
                                yAxis: {
                                    labels: {
                                        formatter: function () {
                                            return this.value.charAt(0);
                                        }
                                    }
                                }
                            }
                        }]
                    }
                }       
            }
        }
    })
</script>