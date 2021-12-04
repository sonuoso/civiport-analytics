$(document).ready(function () {
  $("#transactions").DataTable({
    info: false,
    ordering: false,
    pageLength: 20,
    lengthChange: false,
    dom: "rtp", //p - pagination, t - table, r - display
    columnDefs: [
      {
        targets: [0,3,5],
        searchable: false,
      },
    ],
  });
  $("#transactions_chain").DataTable({
    info: false,
    ordering: false,
    pageLength: 20,
    lengthChange: false,
    dom: "rtp", //p - pagination, t - table, r - display
  });
  //Custom Search Bar main_set
  var main_table = $("#transactions").DataTable();
  $("#transactions-search").on("keyup", function () {
    main_table.search(this.value).draw();
  });

  var tx_chain_table = $("#transactions_chain").DataTable();
  $("#transactions_chain_filter.dataTables_filter").append($("#typeSelect"));


  var typeIndex = 1;
  var first_netIndex = 3;
  var second_netIndex = 4;

  $("#transactions_chain th").each(function (i) {
    if ($($(this)).html() == "From") {
      first_netIndex = i;
      return false;
    }
    if ($($(this)).html() == "To") {
      second_netIndex = i;
      return false;
    }
    if ($($(this)).html() == "Type") {
      typeIndex = i;
      return false;
    }
  });
  $.fn.dataTable.ext.search.push(function (settings, data, dataIndex) {
    console.log(settings.nTable.id);
    if (settings.nTable.id !== "transactions_chain"){
        return true;
    }
    var selectedType = $("#typeSelect").val();
    var selectedFirstNet = $("#first_netSelect").val();
    var selectedSecondNet = $("#second_netSelect").val();
    var type = data[typeIndex];
    var first_net = data[first_netIndex];
    var second_net = data[second_netIndex];
    if (
      (selectedType === "" &&
        selectedFirstNet === "" &&
        second_net.includes(selectedSecondNet)) ||
      (type.includes(selectedType) &&
        selectedFirstNet === "" &&
        selectedSecondNet === "") ||
      (type.includes(selectedType) &&
        first_net.includes(selectedFirstNet) &&
        selectedSecondNet === "") ||
      (type.includes(selectedType) &&
        first_net.includes(selectedFirstNet) &&
        selectedSecondNet === "") ||
      (type.includes(selectedType) &&
        first_net.includes(selectedFirstNet) &&
        second_net.includes(selectedSecondNet)) 
    ) {
      return true;

    }
    return false;
  });

  $("#typeSelect,#first_netSelect,#second_netSelect").change(function (e) {
      tx_chain_table.draw();
  });

  table.draw();
});
