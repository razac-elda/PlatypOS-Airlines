document.addEventListener('DOMContentLoaded', function () {
    $("#RoundtripRadioInput").click(function () {
        $("#DateEnd").attr("disabled", false);
    });
    $("#OnewayRadioInput").click(function () {
        $("#DateEnd").attr("disabled", true);
    });
});