$(document).ready(function(){
    let is_Active = null;
    $('.movie > tbody > tr').click(function() {
        if(is_Active){
            $(is_Active).removeClass("table-active")
            is_Active = this
        }
        else{
            is_Active = this
        }
        if(this.classList.contains("table-active")){
            $(this).removeClass("table-active");
        }
        else{
            $(this).addClass("table-active");
        }

    });
    $('.btn-danger').click(function (){
        let elem = document.getElementById(this.value);
       $.ajax({
            url: window.url,
            method: 'post',
            dataType: 'html',
            type: "delete",
            data: $(this.parentNode).serialize(),
            success: function(data){


                elem.parentNode.removeChild(elem);
                if (data['new']){
                    elem.parentNode.appendChild(data['elem'
                    ]);
                }

	}
});
    });
});
