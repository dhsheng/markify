<%inherit file="../base.mako" />
<%block name="title">订单管理</%block>
<%block name="content">
    <div class="row">
        <a href="${request.reverse_url('order.create')}" class="btn btn-success">添加订单</a>
    </div>
    <div class="row">
        <div class="span6">
            <table class="table table-bordered">
        <thead>
        <tr><th>名称</th><th>金额</th><th>客户名称</th><th>状态</th><th>日期</th><th>操作</th></tr>
        <%! from datetime import datetime as dt %>
        <%! import binascii %>
        %for order in orders:
            <tr>
                <td>${order.name}</td>
                <td>${order.amount}</td>
                <td>${order.customer_name and order.customer_name or u'未知'}</td>
                <td>
                    %if order.state == 'N':
                        <span class="label label-info">未付款</span>
                    %elif order.state == 'F':
                        <span class="label label-danger">已作废</span>
                    %elif order.state == 'S':
                        <span class="label label-success">已付款</span>
                    %endif
                </td>
                <td>${dt.fromtimestamp(order.created).strftime('%Y-%m-%d')}</td>
                <td>
                    <a href="/order/edit?id=${binascii.b2a_hex(order.id)}">编辑</a>
                    <a href="/order/view?id=${binascii.b2a_hex(order.id)}">查看</a>
                </td>
            </tr>
        %endfor
        </thead>
    </table>
        </div>
        <div class="span8">

        </div>
    </div>
</%block>
<%block name="javascript">
    <script type="text/javascript">

$('#orders').addClass('active');
    </script>
</%block>