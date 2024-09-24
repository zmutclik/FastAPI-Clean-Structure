$(document).ready(function () {
    $('#table_').DataTable({
        serverSide: true,
        ajax: {
            "url": '/page/users/{{clientId}}/{{sessionId}}/datatables', "contentType": "application/json", "type": "POST",
            "data": function (d) {
                return JSON.stringify(d);
            }
        },
        "paging": false,
        "lengthChange": false,
        "searching": false,
        "ordering": true,
        "info": false,
        "autoWidth": false,
        "responsive": true,
        columns: [
            { "data": "username", "title": "USERNAME", },
            { "data": "email", "title": "EMAIL", },
            { "data": "full_name", "title": "NAMA", },
            { "data": "unlimited_token_expires", "title": "UNLIMITED TOKEN", },
        ],
    });

    $("#btnTambah").on("click", function () {
      window.location.href = '/page/users/{{clientId}}/{{sessionId}}/{{app_version}}/form';
    });
});