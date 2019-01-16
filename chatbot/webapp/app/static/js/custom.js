var socket = io.connect('http://localhost:5000/');



socket.on('answer',function(data) {
// append the bot repsonse to the div

  $('.chat-container').append(`<div class="chat-message bot-message" id="bMsg">
  ${data.message}
  </div>`)
  $('.chat-container').scrollTop(1000);

  // remove the loading indicator
  $( "#loading" ).remove();
});


    $('#target').on('submit', function(e){
            e.preventDefault();
            //alert("hi");
            const input_message = $('#input_message').val()
            // return if the user does not enter any text
            if (!input_message) {
              return
            }

            $('.chat-container').append(`
                <div class="chat-message human-message">
                    ${input_message}
                </div>
            `)

            // loading
            $('.chat-container').append(`
                <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
                    <b>...</b>
                </div>
            `)

            // clear the text input
            $('#input_message').val('')


            // send the message
            alert("Hi")
            //alert( {{course_info.name}} )
            socket.emit('question',{question:input_message,email_id: {{course_info.email_id}}, name: {{course_info.name}}, course_id: {{course_info.course_id}} })
            //submit_message(input_message)
        });
