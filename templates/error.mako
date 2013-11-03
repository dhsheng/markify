<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>出错了！！！</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <link rel="stylesheet" type="text/css" href="${request.static_url('stylesheets/bootstrap.min.css')}" />
    <style type="text/css">

      html,
      body {
        height: 100%;

      }

      #wrap {
        min-height: 100%;
        height: auto !important;
        height: 100%;
        margin: 0 auto -60px;
      }

      #footer {
        background-color: #f5f5f5;
      }


      .container {
        width: auto;
        max-width: 680px;
      }


    </style>

  </head>

  <body>


    <div id="wrap">

      <div class="container">
        <div class="page-header">
          <h1>出错了！！！</h1>
        </div>
        <p class="lead">你正在执行一个错误的操作，或者程序出错了！！点击
            <a href="${referer and referer or ('Referer' in request.request.headers and request.request.headers['Referer'] or '')}">这里</a>返回。</p>
         </div>

    </div>

    <div id="footer">

    </div>

  </body>
</html>
