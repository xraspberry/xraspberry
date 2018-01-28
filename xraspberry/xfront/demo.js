//主要就是ajax部分，这里用到了JQuery中的$.ajax函数，详细用法请参照JQ文档
$.ajax({
    'url':'http://localhost:6666/api/v1/user/login',
    'data':{
        "username":$('#userName').val(),
        "password":$('#password').val(),
    },
    'success':
        function(data){
            switch(data.type){
                case 0:alert('账户不存在');break;
                case 1:{
                    $('#userMsg').children('li').eq(2).find('span').html(' '+data.gouwuchenum+' ');
                    $('#loginMsg li').eq(1).empty().html('<span>'+data.name+'</span>');
                    $('#loginMsg li').eq(2).empty().html('<a href="javascript:tuichu()">退出</a>');
                    $('.login').animate({right:-180,opacity:0},400,function(){
                        $(this).css('display','none'); });
                    break;
                }
                case 2:alert('密码错误');
                break;
            }
        },
    'type':'post',
    'dataType':'json',
});
