<div class="form-group">
    <input class="form-control" type="text"
           value="${product and product.name or ''}"
           name="name" id="name" placeholder="商品名称"/>
</div>
<div class="form-group">
    <input class="form-control" type="text"
           value="${product and product.stock or ''}"
           name="stock" id="name" placeholder="商品数量"/>
</div>
<div class="form-group">
    <input class="form-control"
           value="${product and product.unit or ''}"
           type="text" name="unit" id="name" placeholder="单位"/>
</div>
<div class="form-group">
    <input class="form-control" type="text"
           value="${product and product.amount or ''}"
           name="amount" id="name" placeholder="商品总金额"/>
</div>
${request.xsrf_form_html()}