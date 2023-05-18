current_email = undefined;

document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-form').addEventListener('submit', function(event) {
    event.preventDefault();
    send_email();
  });
  document.querySelector('#emails-view').addEventListener('click', view_email);

  // run the archive function on click
  document.querySelector('.archive').addEventListener('click', function() {
    if (current_email.archived === false) {
      archive(true);
    } else {
      archive(false);
    }
  });

  // Run the reply function
  document.querySelector('.view-email-reply').addEventListener('click', function() {
    compose_email('reply');
  })

  // By default, load the inbox
  load_mailbox('inbox');
});

// Archive or Unarchive and wait for fetch function to finish
async function archive(status) {
  const fetcher = await fetch(`/emails/${current_email.id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: status
    })
  });
  load_mailbox('inbox');
}

function view_email(email_id) {
  // Hide the other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-list').style.display = 'none';
  document.querySelector('#view-email').style.display = 'block';
  document.querySelector('.archive').innerHTML = '';
  document.querySelector('.view-email-reply').innerHTML = '';

  // Fetch the email by id
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    current_email = email;
    console.log(`current email: ${current_email.subject}`);

    // Fill in the Email fields to read
    document.querySelector('.view-email-sender').innerHTML = `<b>From:</b> ${email.sender}`;
    document.querySelector('.view-email-recipients').innerHTML = `<b>To:</b> ${email.recipients}`;
    document.querySelector('.view-email-subject').innerHTML = `<b>Subject:</b> ${email.subject}`;
    document.querySelector('.view-email-time').innerHTML = `<b>Timestamp:</b> ${email.timestamp}<hr>`;
    document.querySelector('.view-email-body').innerHTML = `${email.body}`;

    user = document.querySelector('#user_email').value;
    if (user !== email.sender) {
      // Decide whether to use archive or unarchive button
      const archive_button = document.createElement('button');
      if (email.archived === false) {
        archive_button.innerHTML = 'Archive';
        archive_button.setAttribute("id", "archive");
      } else {
        archive_button.innerHTML = 'Unarchive';
        archive_button.setAttribute("id", "unarchive");
      }
      document.querySelector('.archive').append(archive_button);

      // Make the reply button
      const reply_button = document.createElement('button');
      reply_button.innerHTML = 'Reply';
      document.querySelector('.view-email-reply').append(reply_button);
    }



    // Mark email as read
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
  })
}

function send_email() {
  document.querySelector('#emails-list').innerHTML = '';
  
  // retrieve email information
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;

  // Send the email
  fetch('/emails', {
    method: 'POST', 
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    })
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
    load_mailbox('sent');
  })
}

function compose_email(action) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails-list').innerHTLM = '';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-list').innerHTML = '';
  document.querySelector('#view-email').style.display = 'none';

  // Prefill info if it is a reply
  if (action === 'reply'){
    // Fill in reply fields
    document.querySelector('#compose-recipients').value = `${current_email.sender}`;
    if (current_email.subject.slice(0, 4) !== 'Re: ') {
      document.querySelector('#compose-subject').value = `Re: ${current_email.subject}`;
    } else {
      document.querySelector('#compose-subject').value = `${current_email.subject}`;
    }
    document.querySelector('#compose-body').value = `\n\n\n<hr>On ${current_email.timestamp} ${current_email.sender} wrote:\n${current_email.body}`;
  } else {
    // Clear out composition fields
    document.querySelector('#compose-recipients').value = '';
    document.querySelector('#compose-subject').value = '';
    document.querySelector('#compose-body').value = '';

  }
}

function load_mailbox(mailbox) {
// Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails-list').style.display = 'block';
  document.querySelector('#emails-list').innerHTML = '';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#view-email').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch(`emails/${mailbox}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    
    // List each email
    var i;
    for (i = 0; i < email.length; i++) {
      let subject = email[i].subject;
      let sender = email[i].sender;
      let time = email[i].timestamp;
      let id = email[i].id;

      const li = document.createElement('li');
      li.innerHTML = `<p><b>${sender}</b> ${subject} <span class="email-time">${time}</span></p>`;
      if (email[i].read === true) {
        li.classList.add('read');
      } else {
        li.classList.add('unread');
      }
      li.addEventListener('click', function() {
        view_email(`${id}`);
      });
      document.querySelector('#emails-list').append(li);
    }    
  });
}