$(document).ready(function () {
  $("#transactions").DataTable({
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

  table.draw();
});
