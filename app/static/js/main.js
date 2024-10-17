$(document).ready(function() {
    $('#query-form').submit(function(e) {
        e.preventDefault();
        var query = $('#query').val();
        $.ajax({
            url: '/query',
            method: 'POST',
            data: {query: query},
            success: function(response) {
                $('#ai-response').html('<div class="alert alert-success" role="alert">' + response + '</div>');
            },
            error: function() {
                $('#ai-response').html('<div class="alert alert-danger" role="alert">抱歉,无法处理您的请求。</div>');
            }
        });
    });
});
