<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title><%block name="title">${title}</%block></title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link href="/static/stylesheets/bootstrap.css" rel="stylesheet">
    <style>
body {
     padding-top: 60px;
    color: #333333;
    font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    font-size: 12px;
    line-height: 20px;
}
        .nav > li {
            margin-right: 25px;
        }
        .container {
            width: 85% !important;
        }
        a.brand {
           color: #FFFFFF !important;
        }
    </style>
    <%block name="stylesheet"></%block>
    <link href="" rel="stylesheet">
</head>
<body>
    <%block name="header">
        <div class="navbar navbar-inverse navbar-fixed-top">
            <div class="navbar-inner">
                <div class="container">
                    <button type="button" class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="brand" href="#">markify</a>
                    <div class="nav-collapse collapse">
                        <ul class="nav">
                            <li class="active"><a href="#">订单</a></li>
                            <li><a href="#about">客户</a></li>
                            <li><a href="${request.reverse_url('products')}">产品</a></li>
                            <li><a href="#statictis">统计</a></li>
                            <li><a href="#help">帮助</a></li>
                        </ul>
                    </div>
                    <form action="" class="navbar-search pull-left">
                        <input type="text" placeholder="搜索" class="search-query span3">
                    </form>
                    <ul class="nav pull-right">
                        <li class="divider-vertical"></li>
                        <li class="dropdown">
                            <a data-toggle="dropdown" class="dropdown-toggle" href="#">
                                帐号<b class="caret"></b></a>
                            <ul class="dropdown-menu">
                                <li><a href="#">设置</a></li>
                                <li><a href="#">注销</a></li>
                            </ul>
                        </li>
                    </ul>
                </div>

            </div>
        </div>
    </%block>
<div class="container">
    <%block name="content"></%block>
</div>
<div class="container">
    <%block name="footer"></%block>
</div>
<script type="text/javascript" src="/static/javascripts/jquery-1.8.js"></script>
<script type="text/javascript" src="/static/javascripts/bootstrap.js"></script>

<%block name="javascript"></%block>
</body>
</html>
