
$.extend(true, $.fn.dataTable.defaults, {
    bSort: false,
    bAutoWidth: true,
    bJQueryUI: true,
    bProcessing: true,
    sPaginationType: "full_numbers",
    bServerSide: true,
    bPaginate: true,
    aLengthMenu: [
        [9999],
        [9999],
    ],
    columnDefs: [{
        sClass: "center",
        searchable: false,
        orderable: false,
        bSortable: false,
        targets: -1,
        sWidth: "15%",
        render: function (data, type, row, meta) {
            return '<div class="btn-group" role="group"> <button type="button" class="btn btn-outline-secondary editor_remv">HAPUS</button> <button type="button" class="btn btn-outline-secondary editor_edit">KOREKSI</button> <button type="button" class="btn btn-outline-secondary editor_show">LIHAT</button> </div>'
        }
    }]
});