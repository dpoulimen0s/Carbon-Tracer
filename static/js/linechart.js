<!-- Author: Dimitrios Poulimenos -->
google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ['Year', "World", "United Kingdom", "You"],
          ['2020',  34807259099 ,      329578911,    5.54 ],

        ]);

        var options = {
          title: 'Carbon Emission',
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }