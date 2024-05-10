document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // se o email for enviado 
  document.querySelector('#compose-form').addEventListener('submit', Sending_mail);


  // By default, load the inbox
  load_mailbox('inbox');
});

function clear_body(){

  // esse sao os padroes (ja tem)
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

}
function entry(recipients,recipients,subject,timestamp){

  // Exibir o formulário de composição de e-mail
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emails-view').style.display = 'none';

  // Limpar os campos do formulário
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';


  document.querySelector('#compose-form').value = recipients;
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = timestamp;


 
};

function archived(id){

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })

  clear_body();
}

function unarchiveEmail(id){

  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })  

  clear_body();

}

function view_email(id){
  
  // clear all page
  clear_body();

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // create new div to display mail
      displaydiv = document.createElement('div');

      // read the email
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })

      displaydiv.style.margin = '2px';

    const isArchived  = email.archived;

    const isArchivedLabel = isArchived ? 'Unarchive': 'Archive';

      displaydiv.innerHTML = `
      <p>From: ${email.sender}</p>
      <p>To: ${email.recipients}</p>
      <p>Subject: ${email.subject}</p>
      <p>Timestamp: ${email.timestamp}</p>
      <button class="btn btn-danger" id="entry">Entry</button>
      <button class="btn btn-primary" id="Archived">${isArchivedLabel}</button>
      </br>
      <hr>
      <p>Timestamp: ${email.body}</p>

      `
    document.querySelector('#emails-view').innerHTML = '';
    document.querySelector('#emails-view').append(displaydiv);
    document.querySelector('#emails-view').style.display = 'block';

    
      // Adicionar evento de clique ao botão #entry
    document.querySelector('#entry').addEventListener('click', () => {
        // Passando os parâmetros para a função entry
        entry(email.recipients, email.sender, email.subject, email.timestamp);
      });

    document.querySelector('#Archived').addEventListener('click',() =>{

      if(email.archived){
        unarchiveEmail(email.id);
      }else{
        archived(email.id);
      }
    });
  });
}

// function to get mail
function get_mail(mailbox){

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // iterate over each email
      emails.forEach(email => {

        // create new div to display mail
        const mailDiv = document.createElement('div');
        mailDiv.classList.add('email');

        // set background color based on read status
        if(email.read){
          mailDiv.style.backgroundColor = '#FAFAFA';
        }else{
          mailDiv.style.backgroundColor = '#ffffff';
        }

        // add border and padding
        mailDiv.style.border = '1px solid #ccc';
        mailDiv.style.padding = '10px';
        mailDiv.style.marginBottom = '10px';
        mailDiv.style.border = '1px solid black';
    

        // set content of email div
        mailDiv.innerHTML = `
          <p style="font-weight: bold;">From: ${email.sender}</p>
          <p style="margin-bottom: 5px;">Subject: ${email.subject}</p>
          <p style="margin-bottom: 5px;">Timestamp: ${email.timestamp}</p>
          `;

       // add click event listener to view email details
       mailDiv.addEventListener('click', () => {
        view_email(email.id);
      });
      
      // append email div to emails-view
      document.querySelector('#emails-view').append(mailDiv);

      });
  });

}

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // aqui temos acesso a todos os mailbox
  get_mail(mailbox);

}

function Sending_mail(event){

  event.preventDefault();

  // pegando os valores
  recipients = document.querySelector('#compose-recipients').value;
  subject = document.querySelector('#compose-subject').value;
  body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

  // By default, load the inbox
  load_mailbox('inbox');

}