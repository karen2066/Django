
function addCart(goods_id){
    // $.post('/axf/addCart/?goods_id=' + goods_id, function (msg) {
    //     if(msg.code == 200){
    //         $('#num_'+goods_id).text(msg.c_num)
    //     }else{
    //         alert(msg.msg)
    //     }
    // });

    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/axf/addCart/',
        type: 'POST',
        data:{'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
           if(msg.code == 200){
               $('#num_'+goods_id).text(msg.c_num)
           }else{
               alert(msg.msg)
           }
        },
        error:function(msg){
            alert(goods_id)
            alert('这里有问题')
           alert('请求失败')
        }
    });
}

function subCart(goods_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/axf/subCart/',
        type: 'POST',
        data:{'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (data) {
           if(data.code == 200){
               $('#num_'+goods_id).text(data.c_num)
           }else{
               alert(data.msg)
           }
        },
        error:function(data){
           alert('请求失败')
        }
    });
}

function changeSelectStatus(cart_id){
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/axf/changeSelectStatus/',
        type: 'POST',
        data: {'cart_id': cart_id},
        dataType:'json',
        headers:{'X-CSRFToken': csrf},
        success:function(data){
            if(data.code == '200'){
                if(data.is_select ){
                    $('#cart_id_' + cart_id).html('√')
                }else{
                    $('#cart_id_' + cart_id).html('×')
                }
            }
        },
        error:function (data) {
            alert('请求失败')
        }
    });
}


function change_order(order_id) {
    var csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/axf/changeOrderStatus/',
        type: 'POST',
        data: {'order_id': order_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            if (msg.code == '200') {
                location.href = '/axf/mine/'
            }
        },
        error: function (msg) {
            alert('订单状态修改失败')
        }
    });
}