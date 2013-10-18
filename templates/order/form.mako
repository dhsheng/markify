<div id="form-fields-wrapper" style="margin-top:30px;">
    <div class="controls">
        <label for="name">订单名字</label>
        <input class="span5" type="text" placeholder="输入订单名字" name="name">
    </div>
    <div class="controls">
        <label for="state-normal">
            状态
        </label>
        <label class="checkbox inline">
            <input type="checkbox" id="state-normal" checked="checked" value="N"> 未付款
        </label>
        <label class="checkbox inline">
            <input type="checkbox" id="state-success" value="S"> 已付款
        </label>
        <label class="checkbox inline">
            <input type="checkbox" id="state-failed" value="F"> 已作废
        </label>
    </div>
    <div class="controls" id="orders-wrapper" style="margin-top:20px;">
        <a href="#create-order-item-window"
           role="button" class="btn" data-toggle="modal">添加订单项</a>
        <table class="table table-bordered" id="orders">
        </table>
    </div>

    <div class="controls" style="margin-top: 50px;">
        <input type="button" class="btn btn-success btn-medium" value="保存数据"/>
    </div>
    <div id="create-order-item-window"
         class="modal hide fade span7" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
            <h3 id="title">添加订单项</h3>
        </div>
        <div class="modal-body">
            <div class="controls">
                <div class="controls controls-row">
                    <select name="product" id="product">
                        <option value="-1">请选择商品</option>
                    </select>
                    <input type="text"
                           placeholder="数量"
                           name="count" id="count" style="margin:-6px 0 0 15px;"/>
                </div>
            </div>
            <div class="controls">
                <div class="controls controls-row">
                    <input class="span3" type="text" placeholder="长度">
                    <input class="span3" type="text" placeholder="宽度">
                </div>
            </div>
            <div class="controls">

                <div class="controls controls-row">
                    <input class="span3" type="text" placeholder="喷漆单价">
                    <input class="span3" type="text" placeholder="数量">
                </div>
            </div>
            <div class="controls">

                <div class="controls controls-row">
                    <input class="span3" type="text" placeholder="磨边单价">
                    <input class="span3" type="text" placeholder="数量">
                </div>
            </div>
            <div class="controls">

                <div class="controls controls-row">
                    <input class="span3" type="text" placeholder="钻空单价">
                    <input class="span3" type="text" placeholder="数量">
                </div>
            </div>

            <div class="controls">

                <div class="controls controls-row">
                    <input class="span3" type="text" placeholder="钢化单价">
                    <input class="span3" type="text" placeholder="数量">
                </div>
            </div>

            <div class="controls">
                <div class="controls controls-row">
                    <input class="span3" type="text" placeholder="倒角单价">
                    <input class="span3" type="text" placeholder="数量">
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-danger" data-dismiss="modal" aria-hidden="true">取消</button>
            <button class="btn btn-success">添加</button>
        </div>
    </div>
    <style type="text/css">
        label.inline {
            padding-top: 0 !important;
        }

        .controls {
            margin-bottom: 5px !important;
        }

        #create-order-item-window input[type="text"] {
            margin-bottom: 2px !important;
        }

    </style>


</div>