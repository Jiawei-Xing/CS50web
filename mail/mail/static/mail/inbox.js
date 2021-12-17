document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // By default, load the inbox
  load_mailbox('inbox');
  
  // sent email by submit
  document.querySelector('form').addEventListener('submit', function(event) {
      
      // POST /emails
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: document.querySelector('#compose-recipients').value,
            subject: document.querySelector('#compose-subject').value,
            body: document.querySelector('#compose-body').value,
        })
      })
      .then(response => response.json())
      .then(result => {
          // Print result
          console.log(result);
      });
      
      // load sent
      event.preventDefault();
      load_mailbox('sent');
  });
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function reply_email(email) {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // fill out composition fields
  document.querySelector('#compose-recipients').value = email.sender;
  
  if (email.subject.slice(0, 3) !== "Re:") {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
  }
  else{
      document.querySelector('#compose-subject').value = `${email.subject}`;
  }

  document.querySelector('#compose-body').value = `On ${email.time} ${email.sender} wrote: ${email.body}`;
}
  
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // show emails inside mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // display emails
      emails.forEach(email => {
        const element = document.createElement('div');
        if (mailbox === 'sent'){
            element.innerHTML = `<hr> <b>To:</b> ${email.recipients}  <b>Subject:</b> ${email.subject}  <b>Time:</b> ${email.timestamp}`;
        }
        else{
            element.innerHTML = `<hr> <b>From:</b> ${email.sender}  <b>Subject:</b> ${email.subject}  <b>Time:</b> ${email.timestamp}`;
        }
        
        // click mail
        element.addEventListener('click', function() {
            console.log('This element has been clicked!');
            
            // change read state
            fetch(`/emails/${email.id}`, {
              method: 'PUT',
              body: JSON.stringify({
                  read: true
              })
            })
            
            // view single email
            document.querySelector('#emails-view').style.display = 'none';
            document.querySelector('#email-view').style.display = 'block';
            document.querySelector('#compose-view').style.display = 'none';
            document.querySelector('#email-view').innerHTML = `<b>From:</b> ${email.sender} <hr> <b>To:</b> ${email.recipients} <hr> 
              <b>Subject:</b> ${email.subject} <hr> <b>Time:</b> ${email.timestamp} <hr> ${email.body} <hr> <button id='reply'>Reply</button>`;
                  
            // reply sent
            document.querySelector('#reply').addEventListener('click', () => reply_email(email));
         
            if (mailbox === 'inbox'){
            
                // archive
                document.querySelector('#email-view').innerHTML += ' <button id="archive">Archive</button>';
                document.querySelector('#archive').addEventListener('click', function() {
                  fetch(`/emails/${email.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: true
                    })
                  })
                  load_mailbox('inbox')
                });
                
                // reply inbox
                document.querySelector('#reply').addEventListener('click', () => reply_email(email));
            }
            
            else if (mailbox === 'archive'){
            
                // unarchive
                document.querySelector('#email-view').innerHTML += ' <button id="unarchive">Unarchive</button>';
                document.querySelector('#unarchive').addEventListener('click', function() {
                  fetch(`/emails/${email.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        archived: false
                    })
                  })
                  load_mailbox('inbox')
                });
                
                // reply inbox
                document.querySelector('#reply').addEventListener('click', () => reply_email(email));
            }
        });
        
        // background color based on read state
        if (email.read){
            element.style.backgroundColor = '#eeeeee'
        }
        
        document.querySelector('#emails-view').append(element);
      });
  });
}


