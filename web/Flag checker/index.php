<!DOCTYPE html>
<html lang=en-us>
   <head>
      <meta charset=utf-8>
      <meta content="text/html; charset=utf-8"http-equiv=Content-Type>
      <link href=https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css rel=stylesheet crossorigin=anonymous integrity=sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ>
      <link href=css/bootstrap.min.css rel=stylesheet media=screen>
      <link href=css/starter-template.css rel=stylesheet media=screen>
      <title>Flag Checker</title>
   </head>
   <body>
      <div class=container>
         <div class=starter-template>
            <h3>Flag Checker</h3>
            Enter your flag:
            <div><input class=form-control id=flag placeholder=Flag><button class="btn btn-info"id=btn-clear type=button>Clear</button><button class="btn btn-success"id=btn-check type=button>Check</button></div>
            <div id=feedback>
               <div class=alert id=alert></div>
            </div>
         </div>
         <script src=https://code.jquery.com/jquery-3.1.1.min.js crossorigin=anonymous></script>
          <script src=https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js crossorigin=anonymous integrity=sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb></script><script src=https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js crossorigin=anonymous integrity=sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn></script>
          <script>function checkFlag() {
            check = Module.cwrap("check", "number", ["string"]), flag = $("#flag").val(), check(flag) ? ($("#feedback").html('<div id="alert" class="alert alert-dismissible alert-success"><button type="button" class="close" data-dismiss="alert">&times;</button><strong>Congratulations!</strong> You can enter this flag in the CTFd.</div>'), $("#feedback").show()) : ($("#feedback").html('<div id="alert" class="alert alert-dismissible alert-danger"><button type="button" class="close" data-dismiss="alert">&times;</button><strong>Incorrect!</strong> Please check your flag again.</div>'), $("#feedback").show())
            }
              
            $("#btn-clear").on("click", (function(e) {
                e.preventDefault(), $("#flag").val(""), $("#feedback").hide()
            })), $("#btn-check").on("click", (function(e) {
                checkFlag()
            })), $(document).keyup((function(e) {
                "Escape" === e.key ? $("#feedback").html("") : "Enter" === e.key && checkFlag()
            }))
          </script>
          <script src=index.js async></script>
      </div>
   </body>
</html>