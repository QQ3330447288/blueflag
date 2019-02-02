/**
 * Created by NIUXINLONG on 2018/5/22.
 */
$(document).ready(function () {
    new WOW().init();
    //    自动播放
    $("#myCarousel").carousel({
        interval: 3000
    });

    $(".side ul li").hover(function () {
        $(this).find(".sidebox").stop().animate({"width": "124px"}, 200).css({
            "opacity": "1",
            "filter": "Alpha(opacity=100)",
            "background": "#ae1c1c"
        })
    }, function () {
        $(this).find(".sidebox").stop().animate({"width": "54px"}, 200).css({
            "opacity": "0.8",
            "filter": "Alpha(opacity=80)",
            "background": "#000"
        })
    });
    //下面可以添加事件
});

function addBoxShadow() {
    $(".addshadow").css("box-shadow","0 4px 10px #888888");
}
function removeBoxShadow() {
    $(".addshadow").css("box-shadow","0 0px 0px #888888");
}
function goTop() {
    $('html,body').animate({'scrollTop': 0}, 600);
}
function qqChat() {
    window.location.href = "tencent://message/?uin=3330447288&Site=Sambow&Menu=yes";
}