<div class="form-group">
    <input class="form-control" type="text"
           value="${customer and customer.name or ''}"
           name="name" id="name" placeholder="客户名称"/>
</div>
<div class="form-group">
    <input class="form-control" type="text"
           value="${customer and customer.phone or ''}"
           name="phone" id="phone" placeholder="电话1"/>
</div>

<div class="form-group">
    <input class="form-control" type="text"
           value="${customer and customer.addition_phone or ''}"
           name="addition_phone" id="addition_phone"
           placeholder="电话2"/>
</div>
<div class="form-group">
    <input class="form-control" type="text"
           value="${customer and customer.email or ''}"
           name="email" id="email" placeholder="电子邮箱"/>
</div>
<div class="form-group">
    <input class="form-control" type="text"
           value="${customer and customer.address or ''}"
           name="address" id="address" placeholder="地址"/>
</div>
${request.xsrf_form_html()}
