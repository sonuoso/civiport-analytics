$(document).ready(function () {
  
  var tokenLabels = pie_data.token_data.token;
  var tokenData = pie_data.token_data.teleports;
  var volumeLabels = pie_data.volume_data.token;
  var volumeData = pie_data.volume_data.volume;

  //Token Transactions Chart
  var pieData = {
    labels: tokenLabels,
    datasets: [
      {
        label: "Teleports by Token",
        data: tokenData,
        backgroundColor: ["rgb(17, 166, 93)", "rgb(38, 166, 219)"],
      },
    ],
  };
  var configTokens = {
    type: "pie",
    data: pieData,
    options: {},
  };
  const tokenChart = new Chart(document.getElementById("tokenChart"), configTokens);

  //Token Transactions Chart
  var pieVolume = {
    labels: volumeLabels,
    datasets: [
      {
        label: "Volume by Token",
        data: volumeData,
        backgroundColor: ["rgb(17, 166, 93)", "rgb(38, 166, 219)"],
      },
    ],
  };
  var configVolume = {
    type: "doughnut",
    data: pieVolume,
    options: {},
  };
  const volumeChart = new Chart(document.getElementById("volumeChart"), configVolume);

});
