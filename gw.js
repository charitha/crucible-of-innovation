var constants = {
    containers: [ "#c1_container","#c2_container","#c3_container"],
    columns:['#banner','#c1_column','#c2_column','#c3_column'],
    colours:["#FF733F","#E64C66","#1AA261"],
    count:0
}


function make_ajax()
{
    $.ajax({
	url:'/getvotes',
	async:false,
	type:"GET",
	success:function(data){
		data = JSON.parse(data);
		console.log(data)
		filter_data(data)	
	   }
	})
	
	
}


function filter_data(data){
    filtered = {"c1":{"team_name":[],"score":[]},"c2":{"team_name":[],"score":[]},"c3":{"team_name":[],"score":[]}}
    $.each(data,function(category_name,element){
        $.each(element,function(index,tuple){            
            filtered[category_name]["team_name"].push("team# "+tuple[0])
            filtered[category_name]["score"].push(tuple[1])
        })
    })
}



function get_chart_objects()
{
    chart_objects = {}
    //Initial drawing of the charts
    for (var i = 1; i <= 3; i++) {        
        var options = get_chart_options({"categories":filtered["c"+i]["team_name"],colour:constants.colours[i-1]})
        $(constants.containers[i-1]).highcharts(options)
        chart_objects["c"+i] = $(constants.containers[i-1]).highcharts()
    };
}

function set_data()
{
    make_ajax();
	get_chart_objects();
	console.log("here")
    for (var i = 1; i <= 3; i++) {      
        chart_objects["c"+i].series[0].setData(filtered["c"+i]["score"])
    };
    setTimeout(set_data,10000)
}

function automatic_scrolling(){

    console.log("Inside automatic scrolling")
    count = constants.count % 4;

    $(constants.columns[(count+1) % 4]).hide()
    $(constants.columns[(count+2) % 4]).hide()
    $(constants.columns[(count+3) % 4]).hide()
    
    $(constants.columns[count]).show(400,function(){
        $('body').scrollTo(constants.columns[count],{duration:'slow'})    
    })
    
    constants.count = constants.count + 1;
    setTimeout(automatic_scrolling,8000)
}

make_ajax()
get_chart_objects()
set_data()
automatic_scrolling()