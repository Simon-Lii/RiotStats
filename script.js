$(document).ready(function() {

  var HORIZONTAL = false;   // `false` for vertical (column) chart, `true` for horizontal bar
  var STACKED = false;  // `false` for individual bars, `true` for stacked bars

  var TITLE = 'Distribution of gold per min per summoner in your elo';

  var LABELS = 'district';  // Column to define 'bucket' names (x axis)

  var SERIES = [  // For each column representing a series, define its name and color
    {
      column: 'nonlearner',
      name: 'Total gold per min',
      color: '#40a8c3',
      radius: 0,
      order: 1,
      type: 'line'
    },
    {
      column: 'learner',
      name: 'Your gold per min',
      color: 'red',
      type: 'line',
      radius: 0,
      order: 5,
    }
  ];

  var X_AXIS = 'Gold per min';  // x-axis label and label in tooltip
  var Y_AXIS = 'Probability density'; // y-axis label and label in tooltip

  var SHOW_GRID = true; // `true` to show the grid, `false` to hide
  var SHOW_LEGEND = true; // `true` to show the legend, `false` to hide

  // Read data file and create a chart
  d3.csv('data.csv').then(function(rows) {

    var datasets = SERIES.map(function(el) {
      return {
        label: el.name,
        labelDirty: el.column,
        backgroundColor: el.color,
        type: el.type,
        data: [],
        radius: el.radius,
        order: el.order
      }
    });

    rows.map(function(row) {
      datasets.map(function(d) {
        d.data.push(row[d.labelDirty])
      })
    });

		var barChartData = {
      labels: rows.map(function(el) { return el[LABELS] }),
			datasets: datasets
    };

    var ctx = document.getElementById('container').getContext('2d');

    new Chart(ctx, {
      type: 'bar', //HORIZONTAL ? 'horizontalBar' : 'bar', 
      data: barChartData,
      
      options: {
        title: {
          display: true,
          text: TITLE,
          fontSize: 14,
        },
        legend: {
          display: SHOW_LEGEND,
        },
        scales: {
          xAxes: [{
            stacked: STACKED,
            scaleLabel: {
              display: X_AXIS !== '',
              labelString: X_AXIS
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              beginAtZero: true,
              callback: function(value, index, values) {
                return value.toLocaleString();
              }
            }
          }],
          yAxes: [{
            stacked: STACKED,
            beginAtZero: true,
            scaleLabel: {
              display: Y_AXIS !== '',
              labelString: Y_AXIS
            },
            gridLines: {
              display: SHOW_GRID,
            },
            ticks: {
              beginAtZero: true,
              callback: function(value, index, values) {
                return value.toLocaleString()
              }
            }
          }]
        },
        tooltips: {
          displayColors: false,
          callbacks: {
            label: function(tooltipItem, all) {
              return all.datasets[tooltipItem.datasetIndex].label
                + ': ' + tooltipItem.yLabel.toLocaleString();
            }
          }
        }
      }
    });

  });

});