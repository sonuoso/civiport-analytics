$(document).ready(function () {
  $("#transactions_chain").DataTable({
    info: false,
    ordering: false,
    pageLength: 20,
    lengthChange: false,
    dom: "rtp", //p - pagination, t - table, r - display
  });
  
  var tx_chain_table = $("#transactions_chain").DataTable();
  $("#transactions_chain_filter.dataTables_filter").append($("#netSelect"));

  var netIndex = 1;

  $("#transactions_chain th").each(function (i) {
    if ($($(this)).html() == "From/To") {
      netIndex = i;
      return false;
    }
  });
  $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {

    var selectedSecondNet = $("#netSelect").val();
    var second_net = data[netIndex];
    if (
      (selectedSecondNet === "" || second_net.includes(selectedSecondNet))
    ) {
      return true;
    }
    return false;
  });

  $("#netSelect").change(function (e) {
      tx_chain_table.draw();
  });

  tx_chain_table.draw();
});
