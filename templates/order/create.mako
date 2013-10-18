<%inherit file="../base.mako" />
<%block name="title">添加订单</%block>
<%block name="content">
    <form action="${request.reverse_url('order.create')}">
    ${request.xsrf_form_html()}
    <%include file="form.mako" />

    </form>
</%block>