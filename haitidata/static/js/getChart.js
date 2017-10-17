var dict_title_tc = {0:"Bar",1:"Pie", 2:"Donut", 3:"Line"};
var dict_title_agg = {0:"Sum",1:"Mean",2:"Count", 3:"Max", 4:"Min"};

var loading = false;

function get_chart_detail(){
    var id = "chart_area_plain"
    //create area for chart
    var createChartArea =  function() {
        var chartArea = document.getElementById(id);
        chartArea.style= "display:table; height:100%; width:100%";
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
     chartArea.style= "display:table; width:100%";
 };
 // update chart
 var replaceChart = function(){
     doc_chart = document.getElementById(id);
     if(doc_chart.childElementCount >= 1){
         doc_chart.removeChild(doc_chart.childNodes[1]);
         createChartArea();
      };
 };

  var createCog = function(){
    var cog_div = document.createElement("div");
    cog_div.innerHTML = '<i class="fa fa-cog fa-spin fa-3x fa-fw"></i><span>Loading data...</span>';
    cog_div.setAttribute("id", "rotella");
    cog_div.setAttribute("style", "display:flex;justify-content:center;align-items:center;");
    var doc_chart = document.getElementById(id);
    element = doc_chart.parentNode;
    element.insertBefore(cog_div, doc_chart);
    
  };

 if (document.getElementById("id_title").value == ""){
     document.getElementById("chart_title").innerHTML = suggestedTitle;
     }else document.getElementById("chart_title").innerHTML = document.getElementById("id_title").value;
if (loading == false) {
 loading = true;
 createCog();
 createChartArea();
 replaceChart();
 attachAbstract();
 getCsv(csv_url, category, quantity, agg, chart_type, id);
}
}
