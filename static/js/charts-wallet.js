$(document).ready(function () {
  
  var tokenLabels = wallet_chart.wallet_data.token;
  var tokenData = wallet_chart.wallet_data.teleports;
  var volumeLabels = wallet_chart.volume_data.token;
  var volumeData = wallet_chart.volume_data.volume;

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
  const walletTeleports = new Chart(document.getElementById("walletTeleports"), configTokens);

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
  const walletVolume = new Chart(document.getElementById("walletVolume"), configVolume);

});
