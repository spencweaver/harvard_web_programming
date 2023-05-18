document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.message_button').forEach(button => {
        button.onclick = () => {
            messageFriend(button.dataset.message);
        }
    });
});


function messageFriend(user_id) {
    console.log(user_id);

    document.querySelector(`.message_div_${user_id}`).innerHTML = '';

    const form = document.createElement("form");
    form.setAttribute("id", "message_form");

    const input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("placeholder", "Message");

    const send = document.createElement("input");
    send.setAttribute("type", "submit");
    send.setAttribute("value", "Send");


    form.appendChild(input);

    document.querySelector(`.message_div_${user_id}`).append(form);
}