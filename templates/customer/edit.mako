<%inherit file="../base.mako" />
<%block name="title">编辑 ${customer.name}</%block>
<%block name="content">
    <form action="${request.reverse_url('customer.edit')}" method="POST" id="update-form">

<%include file="form.mako" />
    <%! import binascii %>
    <input type="hidden" value="${customer and binascii.b2a_hex(customer.id) or ''}" name="id" id="id" />
    <input type="submit" value="更新" class="btn btn-success" />
    <a href="${request.reverse_url('customers')}">返回</a>
    </form>
</%block>