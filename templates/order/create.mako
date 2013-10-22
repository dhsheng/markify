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
    (function() {
        $('#add-item').click(function() {
           $('#create-order-item-window').modal('show');
        });
        var order = new Markify.Order();
        $('#confirm-add-item').click(function() {
            if(order.createItem()) {
                $('#cancel-add-item').trigger('click');
            }
        });
        $('#save-order').click(function() {
            order.save();
        });
    })();
</script>
</%block>