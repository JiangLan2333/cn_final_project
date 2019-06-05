function showLoading(){
  $("#loadingBackground").show();
}
function hideLoading(){
  $("#loadingBackground").hide();
}

var tStudentId="";

$(document).ready(function(){
  var testVM = new Vue({
    el: '#rightSideTable',
    data:{
      testItems:{
        "testList":[]
      },
      disabled:{
        "pointer-events": "none"
      },
      abled:{
        "cursor":"pointer",
        "pointer-events": "auto"
      }
    }
  });

  $.ajax({
    type:"post",
    url:"/login",
    contentType: "application/json",
    data:JSON.stringify({}),
    success:function(data){
      hideLoading();
      /*if(data.identity=="student"){
        var a = document.createElement('a');
        a.href = "control/control.html";
        $("body").append(a);
        a.click();
        $(a).remove();
      }
      else */
      if(data.identity=="guest"){
        $("#rightSideForm")[0].addEventListener('submit',function(e){
          showLoading();
          var userData = {"id":$("#id").val(),"password":$("#password").val()};
          $.ajax({
            type:"post",
            url:"/login",
            contentType: "application/json",
            data:JSON.stringify({"id":userData.id}),
            success:function(data){
              var time=new Date();
              userData.password=md5(md5(userData.password + data.salt)+data.salt);
              $.ajax({
                type:"post",
                url:"/login",
                contentType: "application/json",
                data:JSON.stringify({"id":userData.id,"password":userData.password,"time":time.getTime().toString()}),
                  success:function(data){
                    if(data.op=="admin"){
                      var a = document.createElement('a');
                      a.href = "/controlStudent";
                      $("body").append(a);
                      a.click();
                      $(a).remove();
                    }
                    else if(data.op=="addbook"){
                      var a = document.createElement('a');
                      a.href = "/uploadBelongings";
                      $("body").append(a);
                      a.click();
                      $(a).remove();
                    }
                    else if(data.op == "generaluser"){
                      var a = document.createElement('a');
                      a.href = "/controlBelongings";
                      $("body").append(a);
                      a.click();
                      $(a).remove();
                    }
                    else if(data.op=="error"){
                      alert("用户名或密码错误，请重新输入！");
                    }
                    hideLoading();
                  },
                  error:function(){
                    hideLoading();
                    alert("网络拥堵，请稍后再试！");
                  }
              });
            },
            error:function(){
              alert("网络拥堵，请稍后再试！");
            }
          });
          e.preventDefault();
        },false);
      }
    },
    error:function(){
      alert("网络拥堵，请稍后再试！");
    }
  });
});
