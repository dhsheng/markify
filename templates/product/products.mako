<%inherit file="../base.mako" />
<%block name="title">产品列表</%block>
<%block name="content">
<a class="btn btn-success btn-mini" href="#customer-create-form-wrapper" data-toggle="modal">添加</a>


<div class="modal fade" id="customer-create-form-wrapper" tabindex="-1"
role="dialog" aria-labelledby="product-modal"
         aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
                    <h4 class="modal-title">添加商品</h4>
                </div>
                <div class="modal-body">
                    <form action="" id="customer-create-form">
                        <div class="form-group">
                            <input class="form-control" type="text"
                            name="name" id="name" placeholder="商品名称"/>
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="text" name="total" id="name" placeholder="商品数量"/>
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="text" name="unit" id="name" placeholder="单位"/>
                        </div>
                        <div class="form-group">
                            <input class="form-control" type="text" name="amount" id="name" placeholder="商品总金额"/>
                        </div>
                        ${request.xsrf_form_html()}
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-default" data-dismiss="modal">取消</button>
                    <button type="button"  class="btn btn-success">保存</button>
                </div>
            </div>
            <!-- /.modal-content -->
        </div>
        <!-- /.modal-dialog -->
    </div>
 </%block>
 <%block name="javascript"></%block>