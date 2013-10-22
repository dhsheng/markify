var Markify = Markify || {};



Markify.SimpleCache = function() {
    this._dataKey = 'data';
    this._flag = 'success';
    this._cache = {};
}

Markify.SimpleCache.prototype = {

    get: function(key, remote, callback) {
        var val = key in this._cache ? this._cache[key] : null;
        if(null == val && remote) {
            var me = this;
            $.ajax({
                url: key,
                type: 'GET',
                dataType: 'json',
                success: function(response) {
                    if(this._flag in response && response[this._flag]) {
                        me.set(key, response[this._dataKey]);
                        if(callback && typeof callback == 'function') {
                            callback(response[this._dataKey]);
                        }
                    }
                }
            });
        }
    },

    set: function(key, val) {
        this._cache[key] = value;
    }
};


Markify.Order = function() {};


Markify.Order.prototype = {

    items: {},

    table: $('#orders-table'),

    gid: function() {
        return new Date().getTime();
    },

    createItem: function() {
        var prefixs = ['paint', 'edg', 'chamfer', 'steel', 'drill'], price = function(prefix) {
            return prefix + '_price';
            },count = function(prefix) {
            return prefix + '_count';
            }, item = {}, errors = [];
        for(var i= 0, ele=null, p, c, pv, cv, e, len=prefixs.length; i<len; ++i) {
            ele = prefixs[i], p = price(ele), c = count(ele);
            var pe = $('#' + p), ce = $('#' + c);
            pv = parseFloat(pe.val());
            cv = parseFloat(ce.val());
            e = false;
            if(isNaN(pv)) {
                errors.push(pe);
                e = true;
            }
            if(isNaN(cv)) {
                errors.push(ce);
                e = true;
            }
            if(e) {
                continue;
            }
            item[p] = pv;
            item[c] = cv;
        }
        var l = $('#length'), w = $('#width'), c = $('#count'),
            lv, wv, cv;
        if(isNaN(lv = parseFloat(l.val()))) {
            errors.push(l);
        }
        if(isNaN(wv = parseFloat(w.val()))) {
            errors.push(w);
        }
        if(isNaN(cv = parseFloat(c.val()))) {
            errors.push(c);
        }
        if(errors.length) {
            for(var i= 0, len=errors.length; i<len; i++) {
                $(errors[i]).prop('style', 'border: 1px solid #FF0000');
            }
            return null;
        }
        item['id'] = this.gid();
        item['count'] = cv;
        item['length'] = lv;
        item['width'] = wv;
        this.items[item['id']] = item;
        this.insert(item);
        return item;
    },

    insert: function(item) {
        if(item) {
            this.table.removeClass('hide');
        }
        var cells = '<tr><td></td><td></td><td></td><td></td>';
        cells += '<td>' + item['edg_price'] + '</td>';
        cells += '<td>' + item['chamfer_price'] + '</td>';
        cells += '<td>' + item['steel_price'] +  '</td>';
        cells += '<td>' + item['paint_price'] +  '</td>';
        cells += '<td>' + item['drill_price'] +  '</td><td></td><td>';
        cells += '<a href="#" id="del-item-' + item['id'] +  '">删除</a>&nbsp;&nbsp;';
        cells += '<a href="#" id="edit-item-' + item['id'] +  '">修改</a></td></tr>';
        $('#orders-list').append(cells);
    },

    save: function() {
        var items = this.items, data = [];
        for(var id in items) {
            data.push(this.itemToString(items[id]));
        }
        data =  '[' + data.join(',') + ']';
        $.ajax({
            url: '/order/create',
            data: $('#order-form').serialize() + '&items=' + data,
            type: 'POST',
            dataType: 'json',
            success: function(response) {

            }
        })
    },

    itemToString: function(item) {
        var s = [];
        for(var key in item){
            s.push('"' + key + '": ' + item[key]);
        }
        return '{' + s.join(',') + '}';
    }
};
