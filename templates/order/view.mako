<%inherit file='../base.mako' />
<%block name="stylesheet">
<style type="text/css">

    p {
        font-size: 16px;
    }
    td {
        text-align: center !important;
    }
</style>
</%block>
<%! from datetime import datetime as dt %>
<%! import binascii %>
<%block name="title">订单详情</%block>
<%block name="content">
    <div id="order-wrapper">
            <p>
                <span>订单名称: </span>
            <span style="margin-left: 15px;" id="order-name">${order.name}</span>
            </p>

            <p>
                <span>订单金额: </span>
            <span style="margin-left: 15px" id="order-amount">${order.amount}</span>
            </p>
            <p>
                <span>支付状态: </span>
            <span style="margin-left: 15px"  id="order-state">
                %if order.state == 'N':
                        <span class="label label-info">未付款</span>
                    %elif order.state == 'F':
                        <span class="label label-danger">已作废</span>
                    %elif order.state == 'S':
                        <span class="label label-success">已付款</span>
                %endif
            </span>
            </p>
            <p>
                <span>订单日期: </span>
                <span style="margin-left: 15px;">${dt.fromtimestamp(order.created).strftime('%Y-%m-%d')}</span>
            </p>
        <p>
            <span>客户名称: </span>
            <span style="margin-left: 15px;">
                ${order.customer_name and order.customer_name or u'不详'}
            </span>
        </p>
            <p style="margin-top: 15px;margin-bottom: 0px;">
                <span>订单项</span>
            </p>
            <table id="items" class="table table-bordered">
                    <thead>
                    <tr>
                        <td>品种</td>
                        <td>规格</td>
                        <td>数量</td>
                        <td>价格/<sub>m</sub><sup>2</sup></td>
                        <td>磨边/<sub>m</sub><sup>2</sup></td>
                        <td>倒角/<sub>个</sub></td>
                        <td>钢化/<sub>m</sub><sup>2</sup></td>
                        <td>喷漆/<sub>m</sub><sup>2</sup></td>
                        <td>钻孔/<sub>个</sub></td>
                        <td>小计</td>

                    </tr>
                    </thead>
                    <tbody id="items">
                    %for order_item in order.get_items():
                    <tr>
                        <td>${order_item.product_name}</td>
                        <td>${order_item.length}x${order_item.width}</td>
                        <td>${order_item.count}</td>
                        <td>${order_item.price}</td>
                        <td>${order_item.edg_price}x${order_item.edg_count}</td>
                        <td>${order_item.chamfer_price}x${order_item.chamfer_count}</td>
                        <td>${order_item.steel_price}x${order_item.steel_count}</td>
                        <td>${order_item.paint_price}x${order_item.paint_count}</td>
                        <td>${order_item.drill_price}x${order_item.drill_count}</td>
                        <td>${round(order_item.amount, 2)}</td>

                    </tr>
                %endfor
                    </tbody>
                </table>
        <a href="/" class="btn btn-success">返回</a>
    </div>
</%block>
<%block name="javascript">
</%block>