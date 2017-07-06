var getCsv = function(csv_link, category, quantity, agg, chartType, id){
               var data = [];
               d3.csv(csv_link, function(error, csv) {
                        if (error) throw error;
                        csv.forEach(function(row){
                        var qnty_v; var ctgy_v; var i = 0;
                            while (i < Object.keys(row).length){
                                if (Object.keys(row)[i] == quantity){
                                    qnty_v = +Object.values(row)[i]
                                } else if (Object.keys(row)[i] == category){
                                        if (Object.values(row)[i].length >= 20){

                                            ctgy_v = Object.values(row)[i].substring(0, 17) + "...";
                                        } else {
                                            ctgy_v = Object.values(row)[i];
                                        };
                                }
                            i++;
                            };
                            data.push({qnty : qnty_v , ctgy : ctgy_v });
                        })


               var dropZeros = function(dato){
                               return dato.filter(function(d){
                               if (d.qnty !== 0){
                                return d.qnty;
                               }})
               };

               function groupData_sum(dato){
                       return d3.nest().key(function(d) {return d.ctgy;})
                       .rollup(function(v) {return d3.sum(v, function(d) {return d.qnty;});})
                       .entries(dato);
               };

               function groupData_mean(dato){
                       return d3.nest().key(function(d) {return d.ctgy;})
                       .rollup(function(v) {return d3.mean(v, function(d) {return d.qnty;});})
                       .entries(dato);
               };

               function groupData_min(dato){
                       return d3.nest().key(function(d) {return d.ctgy;})
                       .rollup(function(v) {return d3.min(v, function(d) {return d.qnty;});})
                       .entries(dato);
               };

               function groupData_max(dato){
                       return d3.nest().key(function(d) {return d.ctgy;})
                       .rollup(function(v) {return d3.max(v, function(d) {return d.qnty;});})
                       .entries(dato);
               };

               function groupData_count(dato){
                       return d3.nest().key(function(d) {return d.ctgy;})
                       .rollup(function(v) { return v.length;})
                       .entries(dato);
               };

               function descendent(a,b){
                if (a.value < b.value) return 1;
                if (a.value > b.value) return -1;
               return 0;
               }


               var title;
               var dati;
               function aggregateData(data, agg){

                   if (agg == 0){
                        dati = groupData_sum(dropZeros(data)).sort(descendent);
                        title = "Sum";
                   } else if (agg == 1){
                        dati = groupData_mean(data).sort(descendent);
                        title = "Mean";
                   } else if (agg == 2){
                        dati = groupData_count(data).sort(descendent);
                        title = "Count";
                   } else if (agg == 3){
                        dati = groupData_max(dropZeros(data)).sort(descendent);
                        title = "Maximum";
                   } else if (agg == 4){
                        dati = groupData_min(dropZeros(data)).sort(descendent);;
                        title = "Minimum";
                   };
                   return dati;
               };

               function create(chartType){
               if (chartType == 0){
                   aggregateData(data, agg);
                   if (dati.length > 20){
                        var firstSet = dati.slice(0,19);
                        var lastSet = dati.slice(19,).reduce(function(a, b){ return {key: 'others', value: a.value + b.value }});
                        firstSet.push(lastSet);
                        dati = firstSet;
                   };
                   var chartArea = "#" + id;
                   var bar = barChart(category, quantity, title, id)
                   .x('key')
                   .y('value')
                   d3.select(chartArea)
                        .datum(dati)
                        .call(bar);
               } else if (chartType == 1){
                   aggregateData(data, agg)
                   if (dati.length > 10){
                        var firstSet = dati.slice(0,9);
                        var lastSet = dati.slice(9,).reduce(function(a, b){ return {key: 'others', value: a.value + b.value }});
                        firstSet.push(lastSet);
                        dati = firstSet;
                   };
                   var chartArea = "#" + id;
                   var pie = pieChart(category, quantity, title, id)
                   .variable('value')
                   .category('key')
                   d3.select(chartArea)
                      .datum(dati)
                      .call(pie);
               } else if (chartType == 2){
                   aggregateData(data, agg)
                   if (dati.length > 10){
                        var firstSet = dati.slice(0,9);
                        var lastSet = dati.slice(9,).reduce(function(a, b){ return {key: 'others', value: a.value + b.value }});
                        firstSet.push(lastSet);
                        dati = firstSet;
                   };
                   var chartArea = "#" + id;
                   var donut = donutChart(category, quantity, title, id)
                   .variable('value')
                   .category('key')
                   d3.select(chartArea)
                      .datum(dati)
                      .call(donut);
               } else if (chartType == 3){
                   aggregateData(data, agg)
                   if (dati.length > 20){
                        var firstSet = dati.slice(0,19);
                        var lastSet = dati.slice(19,).reduce(function(a, b){ return {key: 'others', value: a.value + b.value }});
                        firstSet.push(lastSet);
                        dati = firstSet;
                   };
                   var chartArea = "#" + id;
                   var line = lineChart(category, quantity, title, id)
                   .x('key')
                   .y('value')
                   d3.select(chartArea)
                      .datum(dati)
                      .call(line);
               }
               };

               create(chartType);
               });
};






