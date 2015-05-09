(function($, carrot){

        var host = 'localhost:8000'

        var overlayDOM = '<div style="position:fixed; right:0px; bottom:0px; left:0px; top:0px;display:none;background:rgba(0,0,0,0.5);z-index:999;"><div style="position: absolute;top: 10px;right: 20px;color: #fff;cursor: pointer;">x</div><iframe src="http://'+host+'/iframe/notifications/'+carrot.app_secret+'/'+carrot.user_identifier+'/" style="width:100%;height:100%;border: 0px;outline: none;"></iframe></div>';

         //'<div style="position: fixed;bottom: 20px;right: 20px;"><div class="notification-nos" style="background: #CC8300;padding: 6px;color: #fff;font-size: 20px;border-radius: 100%;  padding-left: 15px;padding-right: 15px;box-shadow: 10px;box-shadow: #999 0px 0px 10px;cursor: pointer;"></div></div>';
         var handleDOM = ''+
         '<div class="notification-text" style="position: fixed;bottom: 20px;right: 20px;width: 300px;height: 60px;border: 1px solid #5893C5;border-radius: 7px;background: rgba(0, 0, 0, 0.6);padding: 10px;font-weight: bolder;color: #FFFFFF;text-align: center;cursor:pointer;">'+
           '<p>Things have become better since your last login!</p>'+
         '<div class="notification-nos" style="background: #CC8300;padding: 6px;color: #fff;font-size: 20px;border-radius: 100%;  padding-left: 15px;padding-right: 15px;box-shadow: 10px;box-shadow: #999 0px 0px 10px;cursor: pointer;position: absolute;left: -25px;width: 42px;">8</div></div>';

        var notifications_read = function() {
          $.ajax({
              url: 'http://'+host+'/notifications/'+carrot.app_secret+'/'+carrot.user_identifier+'/read',
              dataType: 'jsonp',
              success: function(data){

              },
              error: function(e, a, b) {
                console.log(a);
              }
          });
        }

        var show_notification_handle = function(count) {

          // form notification_count_handle and append to body
          var tempdiv = document.createElement('div')
          tempdiv.innerHTML = handleDOM;
          $(tempdiv).find('.notification-nos').text(''+count);
          var handle = tempdiv.firstChild;
          document.body.appendChild(handle);

          // form overlayDOM shadow DOM and append to body
          tempdiv.innerHTML = overlayDOM;
          var overlay = tempdiv.firstChild;
          document.body.appendChild(overlay);

          // show notifications on click event on handle
          $(handle).bind('click', function(e) {
            // show overlayDOM
            $(overlay).show();
          });

          // set notifications as read when closed. also remove handle
          $(overlay.firstChild).bind('click', function(e) {
            $(overlay).hide();
            notifications_read();
            $(handle).hide();
          });
        }

        $.ajax({
              url: 'http://'+host+'/notifications/'+carrot.app_secret+'/'+carrot.user_identifier+'/count',
              dataType: 'jsonp',
              success: function(data){
                console.log(data);
                if ( parseInt(data.count) > 0 )
                  show_notification_handle(parseInt(data.count));
              },
              error: function(e, a, b) {
                console.log(a);
              }
          });
})(jQuery, carrot);










// function create_frag(htmlStr) {
//     var frag = document.createDocumentFragment(),
//         temp = document.createElement('div');
//     temp.innerHTML = htmlStr;
//     while (temp.firstChild) {
//         frag.appendChild(temp.firstChild);
//     }
//     return frag;
// }
//
// function insert_stuff(num) {
// 	var s = ' ', fragment = create(s);
// 	document.body.insertBefore(fragment,document.body.childNodes[0]);
// }
