<%inherit file="../base.mako" />
<%block name="title">客户管理</%block>
<%block name="content">
    <a style="margin-bottom: 15px;" class="btn btn-success " href="#customer-create-form-wrapper"
       data-toggle="modal">添加</a>
    <div class="modal fade" id="customer-create-form-wrapper" tabindex="-1" style="display:none;"
         role="dialog" aria-labelledby="product-modal"
         aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title">添加客户信息</h4>
                </div>
                <div class="modal-body">
                    <form action="" id="customer-create-form">
                        <div class="form-group">
                            <input class="form-control" type="text"
                                   name="name" id="name" placeholder="客户名称"/>
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="text" name="phone" id="phone" placeholder="电话1"/>
                        </div>

                        <div class="form-group">
                            <input class="form-control" type="text" name="addition_phone" id="addition_phone"
                                   placeholder="电话2"/>
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="text" name="email" id="email" placeholder="电子邮箱"/>
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="text" name="address" id="address" placeholder="地址"/>
                        </div>
                    ${request.xsrf_form_html()}
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
                    <button type="button" id="button-save" class="btn btn-success">保存</button>
                </div>
            </div>
            <!-- /.modal-content -->
        </div>
        <!-- /.modal-dialog -->
    </div>
    <table class="table table-bordered">
    <thead>
    <tr>
        <th>客户名称</th>
        <th>客户电话</th>
        <th>地址</th>
        <th>电子邮箱</th>
        <th>添加日期</th>
        <th>操作</th>
    </tr>
    <%! from datetime import datetime as dt %>
    <%! import binascii %>
    %for customer in customers:
        <tr>
            <td>${customer.name}</td>
            <td>${customer.phone}</td>
            <td>${customer.address}</td>
            <td>${customer.email}</td>
            <td>${dt.fromtimestamp(customer.created).strftime('%Y-%m-%d')}</td>
            <td>
                <a href="/customer/edit?id=${binascii.b2a_hex(customer.id)}">编辑</a>
                <a class="delete-link" data-id="${binascii.b2a_hex(customer.id)}"

                   href="javascript:void(0)">删除</a>
                <a href="/orders?customer_id=${binascii.b2a_hex(customer.id)}">订单</a>
            </td>
        </tr>
    %endfor
    </thead>
    </table>
</%block>
<%block name="javascript">
    <script type="text/javascript">
        $('#customers').addClass('active');
        $('#button-save').click(function () {
            $('#customer-create-form-wrapper').modal('hide');
            $.ajax({
                data: $('#customer-create-form').serialize(),
                url: '${request.reverse_url('customer.create')}',
                type: 'POST',
                dataType: 'JSON',
                success: function (response) {}
            })
        });
        $('.delete-link').click(function() {
             if(!confirm('确认删除？')) {
                    return ;
                }
            var me = $(this), id = me.attr('data-id');
            $.ajax({
                url: '${request.reverse_url('customer.delete')}',
                data: {'id': id},
                type: 'POST',
                dataType: 'json',
                success: function(response) {
                    if(response.success) {
                        $(me).parent().parent().remove();
                    }
                }
            })
        })
    </script>

</%block>