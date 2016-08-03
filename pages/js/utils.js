// api
var CURRENT_URL = "172.18.231.84"

// static
var CURRENT_URL_2 = "localhost"

var TEST_AUTH = "hwb:hwb"

var DEBUG = false


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
    return null;
}
function clearCookie(name) {  
    setCookie(name, "", -1);
}

function getSearch() {
  var url = location.search;
  var theRequest = {};
  if (url.indexOf("?") != -1) {
    var str = url.substr(1);
    strs = str.split("&");
      for(var i = 0; i < strs.length; i ++) {
        theRequest[strs[i].split("=")[0]]=(strs[i].split("=")[1]);
      }
   }
   return theRequest;
}
