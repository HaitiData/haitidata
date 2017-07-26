var dict_title_tc = {0:"Bar",1:"Pie", 2:"Donut", 3:"Line"};
var dict_title_agg = {0:"Sum",1:"Mean",2:"Count", 3:"Max", 4:"Min"};

function get_chart_detail(){
    var id = "chart_area_plain"
    //create area for chart
    var createChartArea =  function() {
        var chartArea = document.getElementById(id);
        chartArea.style= "display:table; height:100%";
    };

    // update chart
    var replaceChart = function(){
        doc_chart = document.getElementById(id);
        if(doc_chart.childElementCount >= 1){
            doc_chart.removeChild(doc_chart.childNodes[1]);
            createChartArea();
         };
    };

    var chartArea = document.getElementById(id);
    createChartArea();
    replaceChart();
    console.log("son qui")
    getCsv(csv_url, category, quantity, agg, chart_type, id);
}

function title_detail(){

    chart_type = dict_title_tc[chart_type]
    return document.getElementById("title_detail").innerHTML = chart_type + " chart based on " + lyr + " layer (Category field: " + category + ", Quantity field: " + quantity + ")";
}

function get_chart_popup(){
 var id = "chart_area";
 //create area for chart
 var createChartArea =  function() {
     var chartArea = document.getElementById(id);
     chartArea.style= "display:table";
 };
 // update chart
 var replaceChart = function(){
     doc_chart = document.getElementById(id);
     if(doc_chart.childElementCount >= 1){
         doc_chart.removeChild(doc_chart.childNodes[1]);
         createChartArea();
      };
 };
 if (document.getElementById("id_title").value == ""){
     document.getElementById("chart_title").innerHTML = suggestedTitle;
     }else document.getElementById("chart_title").innerHTML = document.getElementById("id_title").value;
 createChartArea();
 replaceChart();
 attachAbstract();
 getCsv(csv_url, category, quantity, agg, chart_type, id);
}
