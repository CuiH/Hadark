window.onload = function() {
  var loginCheck = getSearch();
  if (loginCheck['login'] && loginCheck['login'] == 'true') {
    $("#logIn").modal('show');
  } else if (getCookie("username") != null) {
      $("#main-nav").hide();
      $("#name-nav").show();
      $("#name-nav").css("display", "flex");
      $("#userName").text(getCookie("username"));
  }
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
      if (getCookie("username") == null)
          $("#logIn").modal('show');
      else
          //跳转主页面
        window.location.href = "http://" + CURRENT_URL_2 + "/profile.html";
  });
  $("#feature").click(function() {
      window.location.href = "http://" + CURRENT_URL_2 + "/feature.html";
  });
  $("#help").click(function() {
      window.location.href = "http://" + CURRENT_URL_2 + "/help.html";
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
        $(".buttonloader").addClass("active");
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
            $(".buttonloader").removeClass("active");
          },
          error: function(request) {
            console.log(request);
            if (request.status == 400) {
                $(".error.message").empty();
                $(".error.message").append("用户名/邮箱错误");
                $(".error.message").show();
              }
            $(".buttonloader").removeClass("active");
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
        $(".buttonloader").addClass("active");
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
            $(".buttonloader").removeClass("active");
          },
          error: function(request) {
            console.log(request);
            if (request.status == 400) {
              $(".error.message").empty();
              $(".error.message").append("用户名已被使用");
              $(".error.message").show();
            }
            $(".buttonloader").removeClass("active");
          }
        });
      }
    });
    var h = window.innerHeight - $("#main").offset().top;
    $("#main").css("max-height", h   + "px");
}