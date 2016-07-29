window.onload = function() {
	$(".showLogin").click(function() {
			$("#logIn").modal('show');
	});
	$(".showLogon").click(function() {
			$("#logOn").modal('show');
	});
  $("#logOut").click(function() {
      clearCookie("username");
      clearCookie("password");
      $("#name-nav").hide();
      $("#main-nav").show();
  });
  $("#getStart").click(function() {
      if (getCookie("username") == "null")
          $("#logIn").modal('show');
      else
          //跳转主页面
        alert("跳转");
  });
	$('#loginForm').form({
    	on: 'blur',
    	fields: {
      		username: {
        		identifier  : 'username',
        		rules: [{
            		type   : 'empty',
            		prompt : '用户名/邮箱不能为空'
          	}]},
      		password: {
        		identifier  : 'password',
        		rules: [{
            		type   : 'empty',
            		prompt : '密码不能为空'
          	}]}
    	},
    	onSuccess: function (event, fields) {
        if (event != undefined) {
          event.preventDefault();
        }
        $.ajax({
      		url: "http://172.18.231.84:8000/authentication/login",
          type: "POST",
          data: $("#loginForm").serialize(),
          success: function(data) {
            setCookie("username", $("#loginUser").val());
            setCookie("password", $("#loginPw").val());
            $("#main-nav").hide();
            $("#name-nav").show();
            $("#name-nav").css("display", "flex");
            $("#userName").text(getCookie("username"));
            $("#logIn").modal("hide");
            $(".form input").val("");
          },
          error: function(request) {
            console.log(request);
            if (request.status == 400) {
                $(".error.message").empty();
                $(".error.message").append("用户名/邮箱错误");
                $(".error.message").show();
              }
            }
        });
      }
  	});
  	$('#logonForm').form({
    	on: 'blur',
    	fields: {
      		username: {
        		identifier  : 'username',
        		rules: [{
            		type   : 'empty',
            		prompt : '用户名/邮箱不能为空'
          	}]},
      		password: {
        		identifier  : 'password',
        		rules: [{
            		type   : 'empty',
            		prompt : '密码不能为空'
          	}]}
    	},
    	onSuccess: function (event, fields) {
        if (event != undefined) {
          event.preventDefault();
        }
        $.ajax({
          url: "http://172.18.231.84:8000/authentication/logon",
          type: "POST",
          data: $("#logonForm").serialize(),
          success: function(data) {
            setCookie("username", $("#logonUser").val());
            setCookie("password", $("#logonPw").val());
            $("#main-nav").hide();
            $("#name-nav").show();
            $("#name-nav").css("display", "flex");
            $("#userName").text(getCookie("username"));
            $("#logOn").modal("hide");
            $(".form input").val("");
          },
          error: function(request) {
            console.log(request);
            if (request.status == 400) {
              $(".error.message").empty();
              $(".error.message").append("用户名已被使用");
              $(".error.message").show();
            }
          }
        });
    	}
  	});
}

function setCookie(cname, cvalue, exdays = 0) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "";
    if (exdays != 0)
      expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}
function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length, c.length);
    }
    return "null";
}
function clearCookie(name) {  
    setCookie(name, "", -1);
}  