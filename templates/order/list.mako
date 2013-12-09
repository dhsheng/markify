<%inherit file="../base.mako" />
<%block name="title">订单管理</%block>
<%block name="stylesheet">
    <style type="text/css">
        th, td {
            text-align: center !important;
        }
        th {
            cursor: pointer;
        }
    </style>
</%block>
<%block name="content">
    <div class="row">
        <a href="${request.reverse_url('order.create')}"
           style="margin-bottom: 15px;"
           class="btn btn-success">添加订单</a>
        <div>
            <table class="table table-bordered">
        <thead>
        <tr><th>名称</th><th>金额</th><th>客户名称</th><th>日期</th><th>状态</th><th>操作</th></tr>
        <%! from datetime import datetime as dt %>
        <%! import binascii %>
        %for order in orders:
            <tr>
                <td>${order.name}</td>
                <td>${round(order.amount, 2)}</td>
                <td>${order.customer_name and order.customer_name or u'未知'}</td>

                <td>${dt.fromtimestamp(order.created).strftime('%Y-%m-%d')}</td>
                <td id="state-${binascii.b2a_hex(order.id)}">
                    %if order.state == 'N':
                        <span class="label label-info">未付款</span>
                    %elif order.state == 'F':
                        <span class="label label-danger">已作废</span>
                    %elif order.state == 'S':
                        <span class="label label-success">已付款</span>
                    %endif
                </td>
                <td style="width:150px;">
                    <!--<a href="/order/edit?id=${binascii.b2a_hex(order.id)}">编辑</a>-->
                    <a href="/order/view?id=${binascii.b2a_hex(order.id)}">查看</a>&nbsp;&nbsp;
                <div class="btn-group " id="states">
                    <button data-toggle="dropdown" type="button" data-id="${binascii.b2a_hex(order.id)}" id="state-dropdown"
                            class="btn btn-danger btn-mini dropdown-toggle  ${'' if request.get_cookie('username', '') == 'admin' else 'disabled'}">
                        <span id="state-label">修改状态</span><span style="margin-left:3px;" class="caret"></span>
                    </button>
                    <ul role="menu" class="dropdown-menu" id="states-menu">
                        <li id="payment_no" data-id=""><a href="#">未付款</a></li>
                        <li id="payment_yes" data-id=""><a href="#">已付款</a></li>
                        <li id="payment_failed" data-id=""><a href="#">作废</a></li>
                    </ul>
                </div>
                </td>
            </tr>
        %endfor
        </thead>
    </table>
        </div>
    </div>
    <div class="row toolbar" style="margin-top: 20px;">
        <div class="col-lg-7">
            
             <div class="btn-group" id="states" style="padding:0;margin-top:-20px;">
                    <button data-toggle="dropdown" type="button" id="state-dropdown" class="btn btn-default btn-sm dropdown-toggle btn-primary">
                        <span id="state-label">未付款</span><span style="margin-left:3px;" class="caret"></span>
                    </button>
                    <ul role="menu" class="dropdown-menu" id="states-menu">
                        <li id="payment_no"><a href="#">未付款</a></li>
                        <li id="payment_yes"><a href="#">已付款</a></li>
                        <li id="payment_failed"><a href="#">作废</a></li>
                    </ul>
                </div>

              <div class="btn-group" id="order-date" style="padding:0;margin-top:-20px;">
          <button data-toggle="dropdown" type="button" class="btn btn-default btn-sm dropdown-toggle">
            订单日期 <span class="caret"></span>
          </button>
          <ul role="menu" class="dropdown-menu" id="order-date">
            <li id="today"><a href="#">当天</a></li>
            <li id="one-week"><a href="#">一星期内</a></li>
            <li id="two-week"><a href="#">半个月内</a></li>
            <li id="month"><a href="#">一个月</a></li>
          </ul>
        </div>
        <input type="button" id="button-order-1" value="打印出货单" href="/print/order/preview?pt=normal" class="btn btn-default print" style="margin-top:-20px;">

       <input type="button" id="button-order-2" value="打印应收应付单" href="/print/order/preview?pt=check" class="btn btn-default print" style="margin-top:-20px;">

        </div>
    </div>
    <div id="confirm-window" class="modal hide fade span7" tabindex="-1" role="dialog"  aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="title">添加订单项</h3>
        </div>
        <div class="modal-body" id="item-fields-wrapper"></div>
    </div>
</%block>
<%block name="javascript">
    <script type="text/javascript">
    $('#orders').addClass('active');
    $('#states-menu > li').click(function () {
                var me = $(this), id = me.attr('id'), dropdown = $('#state-dropdown'), label = $('#state-' + dropdown.attr('data-id'));
                        //label = $('#state-label');
                var val = '';
                switch (id) {
                    case 'payment_yes':
                        //dropdown.removeClass('btn-primary').removeClass('btn-danger').addClass('btn-success');
                       label.empty().append('<span class="label label-success">已付款</span>');
                        val = 'Y';
                        break;
                    case 'payment_failed':
                        //dropdown.removeClass('btn-success').removeClass('btn-primary').addClass('btn-danger');
                        //label.text('已作废');
                        label.empty().append('<span class="label label-danger">已作废</span>');
                        val = 'F';
                        break;
                    case 'payment_no':
                        //label.text('未付款');
                        label.empty().append('<span class="label label-info">未付款</span>');
                        //dropdown.removeClass('btn-success').removeClass('btn-danger').addClass('btn-primary');
                        val = 'N';
                        break;
                };
                
            });
    </script>
</%block>