import uuid
from textwrap import dedent
from IPython.core.display import display, HTML
from string import Template
import numpy as np

# function to initialize a scatter plot
def init_chart(data,features):
    chart_id = 'mychart-' + str(uuid.uuid4())
    feature_types = {} # map each feature to type
    num_feature_ranges = {}
    for x in features:
        if data[x].dtype in ["int64", "float64"]:
            feature_domain = [min(data[x].dropna()), max(data[x].dropna())]
            if feature_domain[1] == feature_domain[0]:
                 feature_types[x] = "categorical"
            else:
                feature_types[x] = data[x].dtype.name
                num_feature_ranges[x] = feature_domain
        else:
            feature_types[x] = "categorical"
    display(HTML('<script src="/static/components/requirejs/require.js"></script>'))
    display(HTML(Template(dedent('''
      <style>
      body {
        font: 11px sans-serif;
        color: #2A3F5E
      }
      .chart {
        background-color: #E5ECF6;
        display: relative;
      }
      .axis path,
      .axis line {
        fill: none;
        stroke: #2A3F5E;
        shape-rendering: crispEdges;
      }
      .label {
        color: #2A3F5E;
      }
      .selection {
        margin-bottom: 20px;
      }
      .dot {
        stroke: #fff;
        opacity: 0.8;
      }
      .grid line {
        stroke: #fff;
        stroke-opacity: 0.7;
        stroke-width: 2px;
        shape-rendering: crispEdges;
      }
      .grid path {
        stroke-width: 0;
      }
      .tooltip {
        position: absolute;
        font-size: 12px;
        width:  auto;
        height: auto;
        pointer-events: none;
        background-color: white;
        padding: 5px;
      }
    .legend {
        background-color: white;
        position: absolute;
        left: 650px;
        top: 20px;
        width:  auto;
        height: 500px;
      }
      </style>
      <script>
      require.config({
        paths: {
          'd3': 'https://cdnjs.cloudflare.com/ajax/libs/d3/5.16.0/d3.min',
        }
      })

      // If we configure mychart via url, we can eliminate this define here
      define($chart_id, ['d3'], function(d3) {
        return function (figure_id, legend_id, select_id, data, xCat, yCat, sizeCat, axes) {

          var initialFeature = d3.select("#" + select_id).property("value")

          var margin = {top: 40, right: 10, bottom: 50, left: 50},
            width = 650 - margin.left - margin.right,
            height = 400 - margin.top - margin.bottom;

          // append the svg object to the body of the page
          var svg = d3.select('#' + figure_id)
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
              .attr("transform",
                    "translate(" + margin.left + "," + margin.top + ")");

          // X and Y scales and Axis
          var x = d3.scaleLinear()
              .domain(axes["x"])
              .range([0, width]);

          var y = d3.scaleLinear()
              .domain(axes["y"])
              .range([height, 0]);

          // Add X-axis and label
          svg
            .append('g')
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(x))

          svg.append("text")
              .attr("class", "label")
              .attr("x", width / 2)
              .attr("y", height + 35)
              .style("text-anchor", "end")
              .text(xCat);

          // Add Y-axis and label

          svg
            .append('g')
            .call(d3.axisLeft(y));

          svg.append("text")
              .attr("class", "label")
              .attr("x", -(height - 15)/ 2 )
              .attr("y", -30)
              .attr("transform", "rotate(-90)")
              .style("text-anchor", "end")
              .text(yCat);


          // gridlines in x axis function
          function make_x_gridlines() {
              return d3.axisBottom(x)
                  .ticks(5)
          }
          // gridlines in y axis function
          function make_y_gridlines() {
              return d3.axisLeft(y)
                  .ticks(5)
          }

          // add grid lines

          // add the X gridlines
          svg.append("g")
              .attr("class", "grid")
              .attr("transform", "translate(0," + height + ")")
              .call(make_x_gridlines()
                  .tickSize(-height)
                  .tickFormat("")
              )

          // add the Y gridlines
          svg.append("g")
              .attr("class", "grid")
              .call(make_y_gridlines()
                  .tickSize(-width)
                  .tickFormat("")
              )

          // Add the datapoints
          var dots = svg
            .selectAll()
            .data(data)
            .enter()
            .append("circle")

          // Add the tooltip container to the body container
          // it's invisible and its position/contents are defined during mouseover
          var tooltip = d3.select("body").append("div")
              .attr("class", "tooltip")
              .style("opacity", 0);

          // Add the legend container to the body container
          var legend = d3.select("#" + legend_id).attr("y", 0);

          // tooltip mouseover event handler
          var tipMouseover = d => {
              // x and y numeric labels
              let html  = xCat + ": " + Number((d[xCat]).toFixed(3)) + "<br>" + yCat + ": " + Number((d[yCat]).toFixed(3)) + "<br><br>"
              // color feature label
              html += colorFeature + ": " + d[colorFeature]
              tooltip.html(html)
                  .style("left", (d3.event.pageX + 10) + "px")
                  .style("top", (d3.event.pageY - 15) + "px")
                .transition()
                  .style("opacity", .9)

          };

          function updateLegendCat(featureColors) { // create the categorical legend

            var legend = d3.select("#" + legend_id).html("") // clear current legend content
               legend.attr("width", 150)
                .attr("height", 400); // clear current legend content

                legend.append("text")
                    .attr("x", 15)
                    .attr("y", 10)
                    .text(colorFeature)
                    .attr("font-size", "14px")

                let i = 0
                Object.keys(featureColors).forEach(feature => {
                  legend.append("circle")
                    .attr("cx",20)
                    .attr("cy",30 + 20*i)
                    .attr("r", 4)
                    .style("fill", featureColors[feature])
                  legend.append("text")
                    .attr("x", 40)
                    .attr("y", 30 + 20*i )
                    .text(feature)
                    .style("font-size", "14px")
                    .attr("alignment-baseline","middle")
                  i += 1
                })

          }

        function updateLegendNum(domain) { // create the continuous (numerical) legend

            var legend = d3.select("#" + legend_id).html("").attr("height", 700).attr("width", 500)
            var width = 30,
                height = 300;

            // add legend title
             legend.append("text")
                    .attr("x", 15)
                    .attr("y", 10)
                    .text(colorFeature)
                    .attr("font-size", "14px")

            var textHeight = 5;

            var linearGradient = legend.append("defs")
            .append("linearGradient")
            .attr("id", "linear-gradient")
            .attr("gradientTransform", "rotate(90)");

            var color = d3.scaleSequential(d3.interpolatePlasma).domain([0,100])


            for (let i = 0; i <= 100; i += 5)
                linearGradient.append("stop")
                    .attr("offset", i + "%")
                    .attr("stop-color", color(100-i)); // to get the right orientation of gradient


            const legendScale = num => {
                var scale = d3.scaleLinear()
                          .domain([height, 0])
                          .range(domain)
                return Number((scale(num))).toFixed(0)

            }

            legend.append("rect")
                .attr("x", 20)
                .attr("y", 30)
                .attr("width", width)
                .attr("height", height)
                .style("fill", "url(#linear-gradient)");

            for (let i = 0; i <= 5; i += 1) {
             legend.append("text")
                .attr("x", 55)
                .attr("y", 30 + textHeight/2 + ((height - textHeight)/5)*i)
                .text(legendScale(30 + textHeight/2 + ((height - textHeight)/5)*i))
                .style("font-size", "14px")
                .attr("alignment-baseline","middle");
            }

          }

          // tooltip mouseout event handler
          var tipMouseout = d => {
              tooltip.transition()
                  .duration(0) // ms
                  .style("opacity", 0); // don't care about position!
          };

          var sizeScale = d3.scaleLinear()
                          .domain(sizeCat["range"])
                          .range([3,7])

          dots.attr("class", "dot")
            .attr("cx", d => x(d[xCat]) )
            .attr("cy", d => y(d[yCat]) )
            .attr("r", d => sizeScale(d[sizeCat["label"]]))
            .on("mouseover", tipMouseover)
            .on("mouseout", tipMouseout)

          update(initialFeature)

          // A function that update the chart with the new color coding scheme
          function update(feature) {
            colorFeature = feature
            var colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

            var color;
            let type = $feature_types[feature];
            if (type === "categorical") {
                color = d3.scaleOrdinal(colors);
                let featureColors = {}
                dots
                .attr("fill", d => {
                  let dotColor = color(d[feature])
                  featureColors[d[feature]] = dotColor
                  return dotColor
                })
                updateLegendCat(featureColors) // update the legend with the new color map

            } else {
                let feature_domain = $num_feature_ranges[feature]
                color = d3.scaleSequential(d3.interpolatePlasma).domain(feature_domain)

               dots
                .attr("fill", d => {
                  let dotColor = color(d[feature])
                  return dotColor
                })
               updateLegendNum(feature_domain)

            }

          }

          d3.select("#" + select_id).on("change", function(d) {
            // recover the option that has been chosen
            var selectedOption = d3.select(this).property("value")
            // run the updateChart function with this selected option
            update(selectedOption)
        });
      }
      })
      </script>

      ''')).substitute({ 'chart_id': repr(chart_id),
                        'feature_types': repr(feature_types),
                        'num_feature_ranges': repr(num_feature_ranges)})))
    return chart_id

def scatter_plot(data,x_cat,y_cat,axes,features):
    chart_id = init_chart(data,features)
    features_html_options = "".join([ f"<option value ='{x}'>{x}</option>" for x in features ])
    dict_data = data.replace(np.nan, "N/A").to_dict("records")
    size_cat = {
        "label": "n_reads",
        "range": [min(data["n_reads"]), max(data["n_reads"])]
    }

    display(HTML(Template(dedent('''
      <div class="selection">
        <label for="colorFeature"
             style="display: inline-block; width: 240px; text-align: right">
             <span> Color by feature: </span>
      </label>
      <select id=$select_id>
        $options
      </select>
      </div>
      <div style="position: relative">
        <svg id=$figure_id class='chart'></svg>
        <div class="legend"><svg id=$legend_id height=360 width=250></svg></div>
      </div>
      <script>
      require([$chart_id], function(mychart) {
        mychart($figure_id, $legend_id, $select_id, $data, $x_cat, $y_cat, $size_cat,  $axes )
      })
      </script>
      ''')).substitute({
        'chart_id': repr(chart_id),
        'figure_id': repr('fig-' + str(uuid.uuid4())),
        'legend_id': repr('leg-' + str(uuid.uuid4())),
        'select_id': repr('sel-' + str(uuid.uuid4())),
        'data': repr(dict_data),
        'axes': repr(axes),
        'x_cat': repr(x_cat),
        'y_cat': repr(y_cat),
        'size_cat': repr(size_cat),
        'options': repr(features_html_options)

  })))
