
// Affichage des messages
function display_messages() {
  messages.textContent = '';
  // On envoie une requête Ajax pour récupérer la liste des messages
  ajax_request('GET','/commentaires/' + site_name, function() {

    // récupération des données renvoyées par le serveur
    let data = JSON.parse(this.responseText);
    console.log(data)

    // boucle sur les messages
    data.forEach(display_message);
    console.log(data)

  });
}


// Affichage d'un message
function display_message(msg) {
  // pseudo, timestamp, message, date sont les attributs des messages
 console.log(msg)
  // mise en forme du timestamp
  let d = new Date(parseInt(msg[3],10)*1000)
    , date_options = {
        day:'2-digit',
        month: '2-digit',
        year: '2-digit',
        hour:'2-digit',
        minute:'2-digit'
      }
    , s = d.toLocaleString('fr-FR',date_options)
  ;

  // préparation des parties du message
  let html = '<header class="header_commentaires">' + s + ' <b>[&thinsp;'+msg[1]+'&thinsp;]</b> ';
  if ( msg[5] ) html += 'a visité ce site : '+msg[5];
  html += '<span class="delete" title="supprimer ce message">&#x2612;</span>';
  html += '</header>';
  html += '<p>'+msg[4]+'</p>';

  // affichage du message
  let article = document.createElement('article');
  article.innerHTML = html;
  article.dataset.id = msg[0];
  messages.appendChild(article);

  // touche de suppression du message
  let span = article.querySelector('.delete')
  span.addEventListener('click', function() {

    // Affichage du popup de demande de mot de passe
    enter_pwd.value = '';
    enter_pseudo.value = '';
    pwd_request.style.marginTop = window.scrollY + 'px';
    pwd_request.style.display='block';
    pwd_request.style.visibility='visible';
    //show(confirm_pwd)

    // Poursuite de l'opération après entrée du mot de passe
    confirm_pwd.addEventListener('click', function() {

      // demande de suppression du message
      ajax_request('DELETE','/commentaire/' + msg[0],
        JSON.stringify({
        pseudo: enter_pseudo.value,
        password: enter_pwd.value,
        }),
        { 'Content-Type': 'application/json' },
        function() {
      
          // suppression du message
          if ( this.status == 200 ) {
            article.parentNode.removeChild(article);
            messages.style.visibility = n ? 'visible' : 'hidden';

            // On cache le popup
            pwd_request.style.display='none';
          }

          // il y a eu un problème côté serveur
          else {
            alert(this.status+' '+this.statusText);
            console.log(this.status,this.statusText);
            error_message_supprimer.style.display='inline-block';
          }
      display_messages();
      });
    },{once: true});
  });

}


// Création d'un message
function post_message() {
  let body = { site: site_name }
    , headers = { 'Content-Type': 'application/json' }
  ;
  [ 'pseudo', 'password', 'message', 'date'].forEach(k => {
        body[k] = window['input_'+k].value;
  });
  ajax_request('POST','/commentaire', JSON.stringify(body), headers, function() {
    if ( this.status == 200 ) {
      let msg = JSON.parse(this.responseText);
      message_editor.style.display='none';
      display_message(msg);
      messages.style.visibility = 'visible';
    }
    else {
      let errmsg = (this.statusText == "Missing 'email'") ? 'Unknown user' : this.statusText
        , status = (this.statusText == "Missing 'email'") ? 401 : this.status
      ;
      alert(status+' '+errmsg);
      console.log(status,errmsg);
      error_message_commentaire.style.display='inline-block';
    }
  });
}

// Création d'un utilisateur
function post_user() {
  let headers = { 'Content-Type': 'application/json' };
  body = {};
  [ 'user_pseudo', 'email', 'user_password'].forEach(k => {
        body[k] = window['input_'+k]?.value;
  });
  ajax_request('POST','/add_user', JSON.stringify(body), headers, function() {
    if ( this.status == 200 ) {
      let user = JSON.parse(this.responseText);
      creation_user.style.display='none';
      console.log("Utilisateur ajouté")
    }
    else {
      let errmsg = (this.statusText == "??'") ? '??' : this.statusText
        , status = (this.statusText == "??'") ? 401 : this.status
      ;
      alert(status+' '+errmsg);
      console.log(status,errmsg);
    }
  });
}

