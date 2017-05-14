$.getJSON( "executions.json", function( data ) {
  new Morris.Area({
    // ID of the element in which to draw the chart.
    element: 'morrisLine',
    // Chart data records -- each entry in this array corresponds to a point on
    // the chart.
    data: data,
    // The name of the data record attribute that contains x-values.
    xkey: 'Day',
    xLabels: 'day',
    // A list of names of data record attributes that contain y-values.
    ykeys: ['Executions'],
    // Labels for the ykeys -- will be displayed when you hover over the
    // chart.
    // labels: ['Executions'],
    resize: true,
    lineColors: ['#333']
  });
});

// Update totals
$.getJSON( "totals.json", function( data ) {
  $("#total-executions").text(data["TOTAL"])
  $("#successful-executions").text(data["SUCCEEDED"])
  $("#failed-executions").text(data["FAILED"])
  $("#unique-users").text(data["UNIQUE_USERS"])
});
