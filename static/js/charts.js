$(document).ready(function () {
  //Teleport Transactions/Volume on Page Loading
  var teleportLabels = chart_data.day_teleports_data.day;
  var teleportData = chart_data.day_teleports_data.teleports;
  var volumeLabels = chart_data.day_volume_data.day;
  var volumeData = chart_data.day_volume_data.volume;
  
  //Teleport Transactions Chart
  var chartData = {
    labels: teleportLabels,
    datasets: [
      {
        label: "Transactions",
        data: teleportData,
        backgroundColor: "rgb(17, 166, 93)",
        borderColor: "rgb(17, 166, 93)",
      },
    ],
  };
  var configTeleports = {
    type: "bar",
    data: chartData,
    options: {},
  };
  const barChart = new Chart(document.getElementById("barChart"), configTeleports);

  var lineData = {
    labels: volumeLabels,
    datasets: [
      {
        label: "Volume",
        data: volumeData,
        backgroundColor: "rgb(17, 166, 93)",
        borderColor: "rgb(17, 166, 93)",
      },
    ],
  };
  const configVolume = {
    type: "line",
    data: lineData,
    options: {},
  };
  const lineChart = new Chart(document.getElementById("lineChart"), configVolume);

  //Teleport Transactions Button Controls
  $("#teleport_btnDaily").click(function(){
    teleportLabels = chart_data.day_teleports_data.day;
    teleportData = chart_data.day_teleports_data.teleports;
    chartData.labels = teleportLabels;
    chartData.datasets[0].data = teleportData;
    barChart.update();
  });

  $("#teleport_btnWeekly").click(function(){
    teleportLabels = chart_data.week_teleports_data.week;
    teleportData = chart_data.week_teleports_data.teleports;
    chartData.labels = teleportLabels;
    chartData.datasets[0].data = teleportData;
    barChart.update();
  });

  $("#teleport_btnMonthly").click(function(){
    teleportLabels = chart_data.month_teleports_data.month;
    teleportData = chart_data.month_teleports_data.teleports;
    chartData.labels = teleportLabels;
    chartData.datasets[0].data = teleportData;
    barChart.update();
  });

  //Volume Button Controls
  $("#volume_btnDaily").click(function(){
    volumeLabels = chart_data.day_volume_data.day;
    volumeData = chart_data.day_volume_data.volume;
    lineData.labels = volumeLabels;
    lineData.datasets[0].data = volumeData;
    lineChart.update();
  });

  $("#volume_btnWeekly").click(function(){
    volumeLabels = chart_data.week_volume_data.week;
    volumeData = chart_data.week_volume_data.volume;
    lineData.labels = volumeLabels;
    lineData.datasets[0].data = volumeData;
    lineChart.update();
  });

  $("#volume_btnMonthly").click(function(){
    volumeLabels = chart_data.month_volume_data.month;
    volumeData = chart_data.month_volume_data.volume;
    lineData.labels = volumeLabels;
    lineData.datasets[0].data = volumeData;
    lineChart.update();
  });

});
