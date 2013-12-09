<%inherit file="../base.mako" />
<%block name="title">添加订单</%block>
<%block name="content">
    <form action="${request.reverse_url('order.create')}" id="order-form">
    ${request.xsrf_form_html()}
    <%include file="form.mako" />
    </form>
    <%include file="order.item.form.mako.html" />
</%block>


<%block name="javascript">
    <script type="text/javascript" src="/static/javascripts/application.js"></script>
    <script type="text/javascript">
        (function () {
            $('#add-item').click(function () {
                $('#create-order-item-window').modal('show');
            });
            var order = new Markify.Order();
            $('#confirm-add-item').click(function () {
                if (order.createItem()) {
                    $('#cancel-add-item').trigger('click');
                }
            });
            $('#save-order').click(function () {
                order.save();
            });
            $(function () {
                Markify.cache.get(Markify.PRODUCTS_KEY, true, (function (id) {
                    return function (products) {
                        var opts = [];
                        for (var i = 0, p, len = products.length; i < len; i++) {
                            p = products[i];
                            opts.push('<option value="' + p.id + '|' + p.name + '">' + p.name + '</option>');
                        }
                        $(id).append(opts.join(""));
                    }
                })('#product'));
            });

            var ITEMS = ${order.items_to_json(True) or 'null'};
            $('.item-edit').click(function() {
                var id = $(this).attr('data-id'), item = ITEMS[id];
                if(item) {
                    for(var k in item) {
                        $('#' + k).val(item[k]);
                    }
                    $('#create-order-item-window').modal('show');
                }
            });
        })();
    </script>
</%block>