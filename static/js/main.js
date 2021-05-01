

  window.onload = initAll;
  var sendTextBtn;
  var saveExeTwice=true;


console.log("jjjjjjjjjjjjjjjjjjjj");

  function initAll(){
     $(".cont").scrollTop($(".cont")[0].scrollHeight);
    sendTextBtn = document.getElementById('sendText');
    sendTextBtn.onclick=sendText;
}




  function sendText(v){
      var x = document.getElementById("sendID").value;
      x=parseInt(x);
      console.log(x);


    var msg=document.getElementById('sender_data').value;
    var url = '/messanger?data='+msg+'&id='+x;

   var req1 = new XMLHttpRequest();
   req1.onreadystatechange = function(){
     if (this.readyState == 4 && this.status ==200){
       $('.input-box').val('').change();
       $(".chatdiv").append('<div class="inside-cont darker"  style="float:left; width:45%; height:auto;  word-wrap: break-word; border-radius: 30px; margin-left:54%;" ><p>'+msg+'</p><span class="time-left">11:01</span></div>');
        $(".cont").scrollTop($(".cont")[0].scrollHeight);

     }
   };

   req1.open("GET", url , true);
   req1.send();

  }

var chk1;
var chk2;
var oneATtime=0;
var allow;
var status="";



setInterval(function(){
  var x = document.getElementById("sendID").value;

  x=parseInt(x);
     var req4 = new XMLHttpRequest();
     var allow=false
     var url = '/all_msg?id='+x;
     oneATtime=0;
     req4.onreadystatechange = function(){

       if (this.readyState === 4 && this.status ===200){
         var d = JSON.parse(req4.responseText);
         console.log(d);
        lst=d['lst'];
        l1=d['l1'];
        l2=d['l2'];
        rsvPer_data=d['rsv_data'];
        sndPer_data=d['sdn_data'];
        whole_msg_buffer=d['whole_msg_buffer'];
        status=d['status'];
        rsv_name=d['rsv_name'];

      $('.status-bar').html('<p style="font-size:25px; color:#0d1b2a;">'+rsv_name+" - "+status+'</p>');


        oneATtime+=1;
        console.log(oneATtime+"in ready");
          if(oneATtime===1){
            try {
              var lst_val=l2[l2.length-1]
            }
            catch(err) {
              var l;
            }
          console.log("hii yuvraj");
              for (var key in l2){
                  if(rsvPer_data.hasOwnProperty(l2[key])===true){
                    $(".chatdiv").append('<div class="inside-cont" style="float:right; word-wrap: break-word; width:45%; height:auto; border-radius: 30px; margin-right:54%;"><p>'+rsvPer_data[l2[key]]+'</p><span class="time-left">11:01</span></div>');
                    $(".cont").scrollTop($(".cont")[0].scrollHeight);
                    }
                  if (l2[key]===lst_val){
                      allow=true;
                      saveExeTwice=false
                      console.log('now allow')
                    }
                  }
                  chk1=0;
                  if (allow===true){
                  console.log('i am in 2');
                  maxValue1 = l1[l1.length-1];
                  maxValue2 = l2[l2.length-1];

                  if (maxValue1 === undefined){
                    maxValue1=0
                  }

                  if (maxValue2 === undefined){
                    maxValue2=0
                  }


                  console.log(maxValue2);

                  var url2 = '/update_token?m1='+maxValue1+'&m2='+maxValue2;
                  req4.onreadystatechange = function(){
                    if (this.readyState === 4 && this.status === 200){
                      var d = req2.responseText;
                      console.log('ayaga bro ');
                      saveExeTwice=true;

                    }
                  };

                  req4.open("GET", url2 , true);
                  req4.send();

                  }

        }

       }
     };

     req4.open("GET", url , true);
     req4.send();





}, 10000);
