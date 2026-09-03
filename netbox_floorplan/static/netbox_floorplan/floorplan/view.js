import {
    resize_canvas,
    export_svg,
    wheel_zoom,
    stop_pan,
    move_pan,
    start_pan,
    reset_zoom,
    init_floor_plan
} from "./utils.js";

var canvas = new fabric.Canvas('canvas');
window.canvas = canvas;
window.fabricCanvas = canvas;

var mouseDownPos = { x: 0, y: 0 };

function get_custom_meta(opt) {
    if (!opt || !opt.target) return null;
    if (opt.target.custom_meta) return opt.target.custom_meta;
    if (opt.target.group && opt.target.group.custom_meta) return opt.target.group.custom_meta;
    return null;
}

canvas.on('mouse:over', function (options) {
    var meta = get_custom_meta(options);
    if (meta && (meta.object_url || meta.object_id)) {
        if (options.target) options.target.hoverCursor = "pointer";
    }
});

canvas.on('mouse:down', function (opt) {
    var evt = opt.e;
    if (evt) {
        mouseDownPos = { x: evt.clientX, y: evt.clientY };
    }
    start_pan(opt, canvas);
});

canvas.on('mouse:move', function (opt) {
    move_pan(opt, canvas);
});

canvas.on('mouse:up', function (opt) {
    stop_pan(canvas);
    var evt = opt.e;
    var dist = 0;
    if (evt) {
        dist = Math.hypot(evt.clientX - mouseDownPos.x, evt.clientY - mouseDownPos.y);
    }
    if (dist < 10) {
        var meta = get_custom_meta(opt);
        if (meta) {
            var url = meta.object_url;
            var objId = meta.object_id;
            var objType = meta.object_type;
            if (!url && objId) {
                url = (objType === 'rack' ? '/dcim/racks/' : '/dcim/devices/') + objId + '/';
            }
            if (url) {
                if (objType === 'device' && !url.includes('/interfaces/')) {
                    url = url.replace(/\/$/, '') + '/interfaces/';
                }
                window.location.href = url;
            }
        }
    }
});

$(window).resize(function() {
    resize_canvas(canvas, window);
});

canvas.on('mouse:wheel', function (opt) {
    wheel_zoom(opt, canvas);
});

var exportSvgBtn = document.getElementById('export_svg');
if (exportSvgBtn) {
    exportSvgBtn.addEventListener('click', () => {
        export_svg(canvas);
    });
}

let floorplan_id = document.getElementById('floorplan_id').value;
function start_view() {
    init_floor_plan(floorplan_id, canvas, "readonly");
}
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start_view);
} else {
    start_view();
}
