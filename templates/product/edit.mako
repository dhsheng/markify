<%inherit file="../base.mako" />
<%block name="title">商品编辑-${product and product.name or ''}</%block>
<%block name="content">
<form method="POST" action="${request.reverse_url('product.edit')}">
<%include file="form.mako" />
     <%! import binascii %>
    <input type="hidden" id="id" name="id" value="${product and binascii.b2a_hex(product.id) or ''}" />
    <input type="submit" class="btn btn-success" value="保存"/>
        <a   href="${'Referer' in request.request.headers and request.request.headers['Referer'] or ''}">返回</a>
</form>
</%block>