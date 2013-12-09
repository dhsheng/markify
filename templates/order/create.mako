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
    <script type="text/javascript" src="${request.static_url('javascripts/application.js')}"></script>
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
            
            $(function () {
                Markify.cache.get('/customers?', true, (function (id) {
                    return function (customers) {
                        var opts = [];
                        for (var i = 0, c, len = customers.length; i < len; i++) {
                            c = customers[i];
                            opts.push('<option value="' + c.id + '|' + c.name + '">' + c.name + '</option>');
                        }
                        $(id).append(opts.join(""));
                    }
                })('#customers-opt'));
            });
        })();
$('#orders').addClass('active');
    </script>
</%block>