/* Javascript for XBadgeXBlock. */
function XBadgeXBlock(runtime, element) {
    /* Html element that is used to display error messages */
    $('.xblock-editor-error-message', element).html();
    $('.xblock-editor-error-message', element).css('display', 'none');

    var myBadges,myVideo,myQuiz,myFlag,myTitle,SCORE,nBadges,quizPass;

    $.ajax({
        type: "POST",
        url: runtime.handlerUrl(element, 'send_Data'),
        data: JSON.stringify({requested: true}),
        success: function(result) {
            myBadges = result.myBadges;
            myVideo = result.myVideo;
            myQuiz = result.myQuiz;
            myFlag = result.myFlag;
            myTitle = result.myTitle;
            SCORE = 0;
            nBadges = result.nBadges;
            quizPass = result.quizPass;

            //Initial Framework
            var html_String = '<table border = "0" ><tr><td colspan = "2" bgcolor = "#ff9446" width=100%><p id="p_bar" style="color:#ffffff;margin-left:5px;"> Badges Earned: 0/7</p></td></tr>';
            for(var i=1;i<=nBadges;i++){
                html_String += '<tr valign = "top"><td bgcolor = "#ffffff" width="256px" height="256px"><img class = "badge_icon" id = "badge' + i + '" src="" alt="Badge">';
                html_String += '</td><td bgcolor = "#ffffff"><div id="div_des' + i + '" height="256px">';
                html_String += '<p class="description" style="color:#d6d6d6;">' + myTitle[1] + '</p></div></td></tr>';
            }
            html_String += '</table>';
            $("#div_badges", element).html(html_String);

            //Initial Titles
            for(var i=1;i<=nBadges;i++){
                SCORE += myFlag[i-1];
                document.getElementById("badge"+i).src= myBadges[i-1];
                var html_des = '<p class="description"';
                if(myFlag[i-1]!=1){
                    html_des += 'style="color:#d6d6d6;">'+myTitle[i-1]+'</p>';
                }else{
                    html_des += '>'+myTitle[i-1]+'</p>';
                }
                $("#div_des"+i, element).html(html_des);
            }

            document.getElementById("p_bar").innerHTML = 'Badges Earned: '+ SCORE +'/'+nBadges;

            // Activate click functions
            $('#div_des1').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(0)).fadeIn(300);
                });
            });

            $('#div_des2').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(1)).fadeIn(300);
                });
            });
            $('#div_des3').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(2)).fadeIn(300);
                });
            });
            $('#div_des4').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(3)).fadeIn(300);
                });
            });
            $('#div_des5').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(4)).fadeIn(300);
                });
            });
            $('#div_des6').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(5)).fadeIn(300);
                });
            });
            $('#div_des7').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(6)).fadeIn(300);
                });
            });
            $('#div_des8').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(7)).fadeIn(300);
                });
            });

            $('#div_des9').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(8)).fadeIn(300);
                });
            });

            $('#div_des10').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(9)).fadeIn(300);
                });
            });

            $('#div_des11').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(10)).fadeIn(300);
                });
            });

            $('#div_des12').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(11)).fadeIn(300);
                });
            });

            $('#div_des13').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(12)).fadeIn(300);
                });
            });

            $('#div_des14').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(13)).fadeIn(300);
                });
            });

            $('#div_des15').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(14)).fadeIn(300);
                });
            });

            $('#div_des16').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(15)).fadeIn(300);
                });
            });

            $('#div_des17').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(16)).fadeIn(300);
                });
            });

            $('#div_des18').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(17)).fadeIn(300);
                });
            });

            $('#div_des19').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(18)).fadeIn(300);
                });
            });

            $('#div_des20').click(function (e) {
                $(this).fadeOut(function() {
                    $(this).html(show_description(19)).fadeIn(300);
                });
            });

            function show_description(index){
                if(myFlag[index]==0){
                    var html_String = "";
                    if(myVideo[index].length!=0){
                        html_String += "<p><strong>Unwatched Video:</strong></p>";
                        html_String += "<p>"+ myVideo[index]+"</p>";
                    }
                    if(myQuiz[index]==0){
                        html_String += "<p><strong>Have to get >=" + quizPass + "% in Online Quiz.</strong></p>";
                    }
                }else if(myFlag[index]==0){
                    html_String = '<p class="description" style="color:#d6d6d6;"'+'>'+myTitle[index]+'</p>';
                }else{
                    html_String = '<p class="description"'+'>'+myTitle[index]+'</p>';
                }
                return html_String;
            }
        }
    });

    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
