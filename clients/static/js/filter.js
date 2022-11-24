$(document).ready(function(){
    console.log('filter')

    $(".ajaxLoader").hide();

    $(".filter-checkbox").on("click", function(){
        var _filterObj = {};

        _filterObj['csrfmiddlewaretoken']=$('input[name=csrfmiddlewaretoken]').val();

        $(".filter-checkbox").each(function(index, ele){
            var _filterVal=$(this).val();
            var _filterKey=$(this).data('filter');
            _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
                return el.value;
            });
        });
        console.log(_filterObj);

        $.ajax({
            url:'/filter-data',
            data:_filterObj,
            dataType:'json',
            beforeSend:function(){
                $(".ajaxLoader").show();
                $(".dives").hide();
            },
            success:function(res){
//                console.log(res.data);
                $("#filterProducts").html(res.data);
                $(".ajaxLoader").hide();
                $("#amount").html(res.amount)
//                console.log(res.amount)
                $(".dives").show();
            }
        });
    });
});