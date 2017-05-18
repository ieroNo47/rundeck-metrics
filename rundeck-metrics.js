var area_graph

$.getJSON( "executions.json", function( data ) {
  area_graph = new Morris.Area({
    // ID of the element in which to draw the chart.
    element: 'morrisLine',
    // Chart data records -- each entry in this array corresponds to a point on
    // the chart.
    data: data,
    // The name of the data record attribute that contains x-values.
    xkey: 'Day',
    xLabels: 'day',
    xLabelAngle: 35,
    // A list of names of data record attributes that contain y-values.
    ykeys: ['Succeeded', 'Failed'],
    // Labels for the ykeys -- will be displayed when you hover over the
    // chart.
    labels: ['Succeeded', 'Failed'],
    resize: true,
    lineColors: ['#0DC695', '#F25654']
  });
});

// Update totals
$.getJSON( "totals.json", function( data ) {
  $("#total-executions").text(data["TOTAL"])
  $("#successful-executions").text(data["SUCCEEDED"])
  $("#failed-executions").text(data["FAILED"])
  $("#unique-users").text(data["UNIQUE_USERS"])
});

function update(){
  $.getJSON( "executions.json", function( data ) {
    area_graph.setData(data);
  });

  $.getJSON( "totals.json", function( data ) {
    $("#total-executions").text(data["TOTAL"])
    $("#successful-executions").text(data["SUCCEEDED"])
    $("#failed-executions").text(data["FAILED"])
    $("#unique-users").text(data["UNIQUE_USERS"])
  });
}

// Update every 10 minutes
setInterval(update, 600000);