<%inherit file="../base.mako" />
<%block name="title">产品列表</%block>
<%block name="content">
    <a class="btn btn-success btn" style="margin-bottom: 15px;" href="#product-create-form-wrapper" data-toggle="modal">添加</a>


    <table class="table table-bordered">
        <thead>
        <tr>
            <th>商品名称</th>
            <th>库存</th>
            <th>总价</th>
            <th>添加日期</th>
            <th>操作</th>

        </tr>
        </thead>
    <tbody>
    <%! import binascii %>
    <%! from datetime import datetime as dt %>
    %for product in products:
        <tr>
            <td>${product.name}</td>
            <td>${product.stock}</td>
            <td>${product.amount}</td>
            <td>${dt.fromtimestamp(product.created).strftime('%Y-%m-%d')}</td>
            <td>
                <a href="${request.reverse_url('product.edit')}?id=${binascii.b2a_hex(product.id)}">编辑</a>
                <a class="delete-link" data-id="${binascii.b2a_hex(product.id)}" href="#">删除</a>
                <a href="${request.reverse_url('orders')}?product_id=${binascii.b2a_hex(product.id)}">订单</a>
            </td>
        </tr>
    %endfor

    </tbody>
    </table>
</%block>
<%block name="javascript">
    <script type="text/javascript">
        $('#products').addClass('active');
        $('#button-save').click(function () {
            $('#product-create-form-wrapper').modal('hide');
            $.ajax({
                data: $('#product-create-form').serialize(),
                url: '${request.reverse_url('product.create')}',
                type: 'POST',
                dataType: 'JSON',
                success: function (response) {
                }
            });
        });
        $('.delete-link').click(function () {
                if(!confirm('确认删除？')) {
                    return ;
                }
                var me = $(this), id = me.attr('data-id');
                $.ajax({
                    url: '${request.reverse_url('product.delete')}',
                    data: {'id': id},
                    type: 'POST',
                    dataType: 'json',
                    success: function (response) {
                        if (response.success) {
                            $(me).parent().parent().remove();
                        }
                    }
                })
            });
    </script>
    <div class="modal fade" id="product-create-form-wrapper" tabindex="-1"
         role="dialog" aria-labelledby="product-modal" style="display:none;"
         aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title">添加商品</h4>
                </div>
                <div class="modal-body">
                    <form action="" id="product-create-form">
                        <%include file="form.mako" />
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
                    <button type="button" class="btn btn-success" id="button-save">保存</button>
                </div>
            </div>
            <!-- /.modal-content -->
        </div>
        <!-- /.modal-dialog -->
    </div>
</%block>