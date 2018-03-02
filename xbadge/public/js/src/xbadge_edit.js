/* Javascript for edit view. */
function XBadgeXBlockEdit(runtime, element) {
    
    /* Html element used to alert users, in case of an error */
    $('.xblock-editor-error-message', element).css('display', 'none');
    $('.xblock-editor-error-message', element).css('color', 'red');

    /* Click event for Cancel button, while in the edit mode */
    $(element).find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });

    /* Click event for Save button, while in the edit mode */
    /* Gets all the input values and sends them back to model */

    var myTitle,myCourseNum,myCourseRun,nBadges,myColor,myGrey,quizPass;
    var videoArr,quizArr,videoEn,quizEn,nVideo,nQuiz;

    var videoMap = [];
    var quizMap = [];

    $(element).find('.save-button').bind('click', function() {

        if(videoEn){
            videoMap = [];
            for(var i=0;i<nVideo;i++){
                iMap = [];
                for (j=0;j<nBadges;j++){
                    try {
                        if(document.getElementById("r"+i+"c"+j).checked){
                            iMap.push(1);
                        }else{
                            iMap.push(0);
                        }
                    }
                    catch(err) {
                        iMap.push(0);
                    }
                }
                videoMap.push(iMap);
            }

            quizMap = [];
            for(var i=0;i<nQuiz;i++){
                iMap = [];
                for (j=0;j<nBadges;j++){
                    try {
                        if(document.getElementById("qr"+i+"c"+j).checked){
                            iMap.push(1);
                        }else{
                            iMap.push(0);
                        }
                    }
                    catch(err) {
                        iMap.push(0);
                    }
                }
                quizMap.push(iMap);
            }
        }

        var temptitle = [];
        var tempcolor = [];
        var tempgrey = [];
        for(i=1;i<=nBadges;i++){
            temptitle.push($("#input_des"+i).val());
            tempcolor.push($("#input_color"+i).val());
            tempgrey.push($("#input_grey"+i).val());
        }
        myTitle = temptitle;
        myColor = tempcolor;
        myGrey = tempgrey;

        quizPass = $('#input_quiz_pass').val();

        var data = {
            'myTitle': myTitle,
            'nBadges':nBadges,
            'myCourseNum':myCourseNum,
            'myCourseRun':myCourseRun,
            'videoMap':videoMap,
            'quizMap':quizMap,
            'videoArr':videoArr,
            'quizArr':quizArr,
            'myColor':myColor,
            'myGrey':myGrey,
            'quizPass':quizPass,
        };

        var handlerUrl = runtime.handlerUrl(element, 'save_Settings');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                window.location.reload(true);
            } else {
                $('.xblock-editor-error-message', element).html('Error: '+response.message);
                $('.xblock-editor-error-message', element).css('display', 'block');
            }
        });
    });

    //Initialization
    $.ajax({
        type: "POST",
        url: runtime.handlerUrl(element, 'send_Edit'),
        data: JSON.stringify({requested: true}),
        success: function(result) {

            myTitle = result.myTitle;
            nBadges = result.nBadges;
            myCourseNum = result.myCourseNum;
            myCourseRun = result.myCourseRun;
            nBadges0 = result.nBadges;
            myCourseNum0 = result.myCourseNum;
            myCourseRun0 = result.myCourseRun;
            videoEn = false;
            videoArr = result.videoArr;
            quizArr = result.quizArr;
            videoMap = result.videoMap;
            quizMap = result.quizMap;
            nVideo = videoArr.length;
            nQuiz = quizArr.length;
            myColor = result.myColor;
            myGrey = result.myGrey;
            quizPass= quizPass;

            UpdateTitle(0,'input_des','#div_title');
            UpdateTitle(0,'input_color','#div_color');
            UpdateTitle(0,'input_grey','#div_grey');
            document.getElementById("select_course_run").disabled = true;
            document.getElementById("button_course_run").disabled = true;
            document.getElementById("button_badge_num").disabled = true;
            document.getElementById("input_badge_num").value= nBadges;

        }
    });

    //Change Course Num
    $(element).find('#button_course_num').bind('click', function() {
        myCourseNum = document.getElementById("input_course_num").value;
        var data={'myCourseNum':myCourseNum};
        var handlerUrl = runtime.handlerUrl(element, 'check_Course');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                var list_run = response.list_run;
                var temp = String(list_run);
                var html_String = '<label class="label setting-label"><strong>Course Run: </strong></label><select id="select_course_run" size="1" disabled>';
                for(var i=0;i<list_run.length;i++){
                    html_String += '<option>'+list_run[i]+'</option>';
                }
                html_String += '</select>';
                $("#div_course_run", element).html(html_String);

                document.getElementById("select_course_run").disabled = false;
                document.getElementById("button_course_run").disabled = false;
            } else {
                $('.xblock-editor-error-message', element).html('Error: '+response.message);
                $('.xblock-editor-error-message', element).css('display', 'block');
            }
        });
    });

    //Select Course Run
    $(element).find('#button_course_run').bind('click', function() {
        if (confirm('Are you sure you want to change Course?')) {
            var e1 = document.getElementById("select_course_run");
            myCourseNum = document.getElementById("input_course_num").value;
            myCourseRun = e1.options[e1.selectedIndex].text;
            alert('Course Changed.\n'+'CourseNum:'+myCourseNum+';\nCourseRun:'+myCourseRun);
        } else {
        }
    });

    //Change Number of Badges
    $(element).on('change', '#input_badge_num', function(){
        UpdateTitle(1,'input_des','#div_title');
        UpdateTitle(1,'input_color','#div_color');
        UpdateTitle(1,'input_grey','#div_grey');
    });

    function UpdateTitle(mode,input_id,div_id) {
        var html_String = "";
        if(div_id == '#div_title'){
            html_String += "<label class='label setting-label'>Badge</label><label class='label setting-label' id='value'>Title</label>";
        }else if(div_id == '#div_color'){
            html_String += "<label class='label setting-label'>Badge</label><label class='label setting-label' id='color_value'>URL of Colorful Images</label>";
        }else{
            html_String += "<label class='label setting-label'>Badge</label><label class='label setting-label' id='grey_value'>URL of Grey Images</label>";
        }
        var value;
        if(mode==1){
            var nGroups = $('#input_badge_num').val();
            for (var i=1;i<=nGroups;i++){
                value = $("#"+ input_id +i).val();
                html_String += "<p><label class='label setting-label'>B"+i+"</label>";
                if (value == null){
                    html_String += "<input style='margin-left: 4px;' class='input setting-input group-value' name='" + input_id +i+"' id='"+input_id+i+"' value='' type='text'></p>";
                }
                else{
                    html_String += "<input style='margin-left: 4px;' class='input setting-input group-value' name='" + input_id +i+"' id='"+input_id+i+"' value='"+value+"' type='text'></p>";
                }
            }
            document.getElementById("button_badge_num").disabled = false;
        }
        else if(mode==0){
            var nGroups = nBadges;
            for (var i=1;i<=nGroups;i++){
                if(div_id == '#div_title'){
                    value = myTitle[i-1];
                }else if(div_id == '#div_color'){
                    value = myColor[i-1];
                }else{
                    value = myGrey[i-1];
                }

                html_String += "<p><label class='label setting-label'>B"+i+"</label>";
                if (value == null){
                    html_String += "<input style='margin-left: 4px;' class='input setting-input group-value' name='" + input_id +i+"' id='"+input_id+i+"' value='' type='text'></p>";
                }
                else{
                    html_String += "<input style='margin-left: 4px;' class='input setting-input group-value' name='" + input_id +i+"' id='"+input_id+i+"' value='"+value+"' type='text'></p>";
                }
            }
        }
        $(div_id, element).html(html_String);

    }


    //Confirm Number of Badges
    $(element).find('#button_badge_num').bind('click', function() {
        if (confirm('Are you sure you want to change Number of Badges?')) {
            nBadges = document.getElementById("input_badge_num").value;
            var temptitle = [];
            var tempcolor = [];
            var tempgrey = [];
            for(i=1;i<=nBadges;i++){
                temptitle.push($("#input_des"+i).val());
                tempcolor.push($("#input_color"+i).val());
                tempgrey.push($("#input_grey"+i).val());
            }
            myTitle = temptitle;
            myColor = tempcolor;
            myGrey = tempgrey;
            alert('The Number of Badges Changed: '+nBadges);
        } else {
        }
    });

    $(element).find('#button_show_map').bind('click',function(){
        var data={
            'nBadges':nBadges,
            'myCourseNum':myCourseNum,
            'myCourseRun':myCourseRun,
        };
        var handlerUrl = runtime.handlerUrl(element, 'show_Map');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                videoArr = response.videoArr;
                quizArr = response.quizArr;
                videoMap = response.videoMap;
                nVideo = videoArr.length;
                nQuiz = quizArr.length;
                var html_String = "<table><p></p><tr><th></th>";
                for(var j=0;j<nBadges;j++){
                    html_String += "<th>B"+(j+1)+"</th>";
                }
                html_String += "</tr>";
                for(var i=0;i<nVideo;i++){
                    html_String += "<tr>";
                    html_String += "<th>"+videoArr[i]+"</th>";
                    for (j=0;j<nBadges;j++){
                        html_String += "<th>"+"<input type='checkbox' id='r"+ i + "c" + j;
                        try{
                            if(videoMap[i][j]==1){
                                html_String += "' checked></th>";
                            }else{
                                html_String += "'></th>";
                            }
                        }
                        catch(err){
                            html_String += "'></th>";
                        }
                    }
                    html_String += "</tr>";
                }
                html_String += "</table>";
                $("#div_map", element).html(html_String);
                videoEn = true;

                html_String = "<table><p></p><tr><th></th>";
                for(var j=0;j<nBadges;j++){
                    html_String += "<th>B"+(j+1)+"</th>";
                }
                html_String += "</tr>";
                for(var i=0;i<nQuiz;i++){
                    html_String += "<tr>";
                    html_String += "<th>"+quizArr[i]+"</th>";
                    for (j=0;j<nBadges;j++){
                        html_String += "<th>"+"<input type='checkbox' id='qr"+ i + "c" + j;
                        try{
                            if(quizMap[i][j]==1){
                                html_String += "' checked></th>";
                            }else{
                                html_String += "'></th>";
                            }
                        }
                        catch(err){
                            html_String += "'></th>";
                        }
                    }
                    html_String += "</tr>";
                }
                html_String += "</table>";
                $("#div_quiz", element).html(html_String);

            } else {
                $('.xblock-editor-error-message', element).html('Error: '+response.message);
                $('.xblock-editor-error-message', element).css('display', 'block');
            }
        });
    });

    $(function () {
        /* Here's where you'd do things on page load. */
    });
}
