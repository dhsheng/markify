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
        <a href="#" id="add-item"
           role="button" class="btn" data-toggle="modal">添加订单项</a>
        <table class="table table-bordered hide" id="orders-table"  style="margin:10px 0;">
            <thead id="orders-table-head">
                    <tr>
                        <th>品种</th>
                        <th>规格</th>
                        <th>数量</th>
                        <th>价格/<sub>m</sub><sup>2</sup></th>
                        <th>磨边/<sub>m</sub><sup>2</sup></th>
                        <th>倒角/<sub>个</sub></th>
                        <th>钢化/<sub>m</sub><sup>2</sup></th>
                        <th>喷漆/<sub>m</sub><sup>2</sup></th>
                        <th>钻孔/<sub>个</sub></th>
                        <th>合计</th>
                        <th>操作</th>
                    </tr>
             </thead>
            <tbody id="orders-list">

            </tbody>
        </table>
    </div>

    <div class="controls" style="margin-top: 50px;">
        <input type="button" class="btn btn-success btn-medium" id="save-order" value="保存数据"/>
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

        .error {
            border: 1px solid #FF000 !important;
        }

    </style>
</div>

