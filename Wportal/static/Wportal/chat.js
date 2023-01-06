document.addEventListener('DOMContentLoaded', function() {
    let user=document.querySelector(".user").innerHTML;
    let user_type=document.querySelector(".user_type").innerHTML;
    StaterMessage(user,user_type);
    var coll = document.getElementsByClassName("collapsible");

    for (let i = 0; i < coll.length; i++) {
        coll[i].addEventListener("click", function () {
            this.classList.toggle("active");

            var content = this.nextElementSibling;

            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
            }

        });
    }
    $("#textInput").keypress(function (e) {
        if (e.which == 13) {
            getResponse(user,user_type);
        }
    });

});

function StaterMessage(user,user_type) {
    let fmessage;
    if(user_type=="Teacher")
    {
        fmessage  = `Hi ${user},Enter the standard to get the notes`
        botHtml='<p class="botText"><span>'+ fmessage+'</span></p>';

    }
    else{
        fmessage = `Hi ${user},Enter the type of the notes,Notes,Questiobank, Studymaterial,Textbook?`;
        botHtml='<p class="botText"><span>'+ fmessage+'</span></p>';
    }

    $("#chatbox").append(botHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);
}


async function getHardResponse(input,user,user_type) {
    let common;
    if((/[a-zA-Z]/).test(input))
      {
       common=input.charAt(0).toUpperCase()+ input.slice(1);
      }
        let flag=true,checking=false;
        let botHtml,result,botResponse;
        if(input=="1" || input=="2" || input=="3"||input=="4"||input=="5" || input=="6" ||input=="7"||input=="8"||input=="9" || input=="10"){
            sta=input
            result="Enter the type of the notes,Notes,Questiobank, Studymaterial,Textbook?"
        }
        else if(common=="Notes" || common=="Questionbank" || common=="Studymaterial" || common=="Textbook")
        {
            type=input
            result="Enter the subject"
        }
        else if(common=="Tamil" || common=="English"|| common=="Maths" || common=="Science" || common=="Social science")
        {
            if(user_type=="Student"){sta="stu"}
            sub=common
            await fetch("/search",{
                method:"POST",
                body:JSON.stringify({
                    sta,
                    sub,
                    type
                })
            })   
            .then(response=>response.json())
            .then(({allnotes})=>{
                if(allnotes.length)
                {
                    allnotes.forEach(note=>{
                    c=note.pdf;
                    unit=note.unit
                    result=c;
                    flag=false
                    botResponse = result;
                    botHtml='<p class="botText"><span><a  href="'+botResponse+'">'+"Unit "+ unit+'</a></span></p>';
                    $("#chatbox").append(botHtml);
                    document.getElementById("chat-bar-bottom").scrollIntoView(true);
                    })
                    StaterMessage(user,user_type);
                }
                else
                {
                    checking=true
                    result="No notes posted"
                }
            }
            );
        }
        else {
            result="Try asking something else!";
        }
        if(flag){
            botResponse = result;
            botHtml = '<p class="botText"><span>' + botResponse + '</span></p>';
            $("#chatbox").append(botHtml);
            document.getElementById("chat-bar-bottom").scrollIntoView(true);
            if(checking){StaterMessage(user,user_type);}

    }
}


function getResponse(user,user_type) {
    let userText = $("#textInput").val();

    if (userText == "") {
        userText = "....";
    }

    let userHtml = '<p class="userText"><span>' + userText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    setTimeout(() => {
        getHardResponse(userText,user,user_type);
    }, 1000)

}

function buttonSendText(sampleText) {
    let userHtml = '<p class="userText"><span>' + sampleText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);


}

function sendButton(user,user_type) {
    getResponse(user,user_type);
}

