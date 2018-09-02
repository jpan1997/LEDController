function send_http_request(type, url, body="") {
   var req = new XMLHttpRequest();
   req.addEventListener("load", function() {
      console.log(this);
   });
   req.open(type, url);
   req.send(body);
}