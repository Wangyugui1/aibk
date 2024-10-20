// 当整个文档（网页）加载完成后，执行以下代码
$(document).ready(function() {
    // 为id为'query-form'的表单添加提交事件监听器
    $('#query-form').submit(function(e) {
        // 阻止表单的默认提交行为
        // 这样可以防止页面刷新，让我们能够使用AJAX发送请求
        e.preventDefault();
        
        // 获取id为'query'的输入框中用户输入的值
        var query = $('#query').val();
        
        // 使用jQuery的ajax方法发送异步请求到服务器
        $.ajax({
            // 设置请求的URL
            url: '/query',
            // 设置HTTP请求方法为POST
            method: 'POST',
            // 设置要发送到服务器的数据
            data: {query: query},
            
            // 如果请求成功，执行这个函数
            success: function(response) {
                // 将服务器的响应放入一个成功提示框中
                // 然后将这个提示框插入到id为'ai-response'的元素中
                $('#ai-response').html('<div class="alert alert-success" role="alert">' + response + '</div>');
            },
            
            // 如果请求失败，执行这个函数
            error: function() {
                // 在id为'ai-response'的元素中显示一个错误提示框
                $('#ai-response').html('<div class="alert alert-danger" role="alert">抱歉,无法处理您的请求。</div>');
            }
        });
    });
});
