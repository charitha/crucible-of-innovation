function get_chart_options(options){
        $categories = options["categories"]   
        $colour = options["colour"]     
        options = {
                chart: {
                    type: 'column'
                },
                title: {
                    text: 'Standings in this category'
                },               
                xAxis: {
                    categories: $categories
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: 'Number of votes'
                    }
                },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                        '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                },
                plotOptions: {
                    column: {
                        pointPadding: 0.2,
                        borderWidth: 0
                    }
                },
                series: [{
                    name:"Category scores",                    
                    data:[],
                    color:$colour
                }]
        }

        return options
}