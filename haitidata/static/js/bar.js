function barChart(cat, qnt, title){
        var width = function(){ return document.getElementById("chart_area").offsetWidth},
            height = 500,
            padding = 5,
            xScale = d3.scaleBand(),
            yScale = d3.scaleLinear(),
            colour = d3.scaleOrdinal(d3.schemeCategory20),
            x,
            y,
            margin = { top: 30, bottom: 30, left: 30, right: 120 },
            floatFormat = d3.format("." + d3.precisionFixed(0.5) + "f"),
            xAxis = d3.axisBottom(xScale),
            yAxis = d3.axisLeft(yScale);

        function my(selection){

          selection.each(function(data) {

            var svg = selection.append('svg')
                .attr("id", "chart_svg")
                .attr("width", width())
                .attr("height", height);

            var g = svg.selectAll("g")
              .data([1]);
            g = g.enter().append("g")
              .merge(g)
                .attr("transform",
                      "translate(" + margin.left + "," + margin.top +")");


            var innerWidth = width() - margin.left - margin.right ;
            var innerHeight = function(){ return height - margin.top - margin.bottom} ;


            xScale
              .domain(data.map(function (d){ return d[x]; }))
              .range([0, (innerWidth - margin.right)]);


            // X axis
            var xAxisG = g.selectAll(".x-axis").data([1]);
            xAxisG.enter().append("g")
                .attr("class", "x-axis")
              .merge(xAxisG)
                .attr("transform", "translate(0," + innerHeight() +")")
                .call(xAxis);

            // labels X axis
            // rotate text if is longer than...

            d3.select(this).select(".x-axis").selectAll("text").each(function(){
                if (this.getBBox().width > (xScale.bandwidth() - (padding*2)))
                    d3.selectAll("text").attr("transform", "rotate(-90)")
                                        .attr("y", 0)
                                        .attr("x", -10)
                                        .attr("dy", ".35em")
                                        .style("text-anchor", "end");
            });

            // adjust margin and x axis title
            var maxh = 0;
            d3.select(this).select(".x-axis").selectAll("text").each(function(){
                if (this.getBBox().width > maxh)
                    maxh = this.getBBox().width;
            });
            margin.bottom = margin.bottom + maxh;
            d3.select(".x-axis").attr("transform", "translate(0," + (innerHeight()) + ")");


            g.append("text")
                .attr("transform", "translate(" + (innerWidth/2) + ", " + (innerHeight() + margin.bottom - 5) + ")")
                .style("font-size", "12px")
                .style("text-anchor", "middle")
                .text(cat);

            yScale
              .domain([0, d3.max(data, function (d){ return d[y] ;})])
              .range([innerHeight(), 0]);

            // Y axis
            var yAxisG = g.selectAll(".y-axis").data([1]);
            yAxisG.enter().append("g")
                .attr("class", "y-axis")
               .merge(yAxisG)
               .call(yAxis);

            //labels Y axis
            var maxw = 0;
            d3.select(this).select(".y-axis").selectAll("text").each(function(){
                if (this.getBBox().width > maxw) {
                    maxw = this.getBBox().width;
                }
            });
            margin.left = margin.left + maxw;
            g.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            var yLabel = function(){
                         if (title == "Count"){
                            return "Count";
                         } else {
                            return qnt;
                         }};

            g.append("text")
                .attr("transform", "rotate(-90)")
                .attr("x", 0 - (innerHeight()/2))
                .attr("y", 0 - (margin.left))
                .attr("dy", "1em")
                .style("font-size", "12px")
                .style("text-anchor", "middle")
                .text(yLabel);

            // bars
            var rects = g.selectAll("rect")
              .data(data);
            rects.exit().remove();
            rects.enter().append("rect")
              .merge(rects)
                .attr("x", function (d){ return xScale(d[x]) + padding; })
                .attr("y", function (d){ return yScale(d[y]); })
                .attr("fill", function(d) { return colour(xScale(d[x])); })
                .attr("width", xScale.bandwidth() - (padding*2))
                .attr("height", function (d){
                  return innerHeight() - yScale(d.value);
                });

            //chart legend
            var legend = svg.selectAll(".legend")
                .data(data)
                .enter().append("g")
                .attr("class", "legend")
                .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

            legend.append("rect")
                .attr("x", width() - 18)
                .attr("width", 18)
                .attr("height", 18)
                .style("fill", function(d) { return colour(xScale(d[x]))} );

            legend.append("text")
                .attr("x", width() - 24)
                .attr("y", 9)
                .attr("dy", ".35em")
                .style("text-anchor", "end")
                .text(function (d){ return d[x] + ": " + floatFormat(d[y]); });

          });
        }

        my.x = function (_){
          return arguments.length ? (x = _, my) : x;
        };

        my.y = function (_){
          return arguments.length ? (y = _, my) : y;
        };

        my.width = function (_){
          return arguments.length ? (width = _, my) : width;
        };

        my.height = function (_){
          return arguments.length ? (height = _, my) : height;
        };

        my.padding = function (_){
          return arguments.length ? (xScale.padding(_), my) : xScale.padding();
        };

        return my;
      }
