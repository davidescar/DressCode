
document.getElementById("formProduct").onsubmit = function(){
	
	var nome = document.getElementById("nome").value;
	var materiale = document.getElementById("materiale").value;
	var prezzo = document.getElementById("prezzo").value;
	var descrizione = document.getElementById("descr").value;
	var categoria = document.getElementById("categ").value;
		
	var valido = true;
	
	var fields = ["Nome","Materiale","Prezzo","Descr","Categ","Taglie","Colori"];
	for(var i = 1; i <= numImm; i++) fields.push("Immagine"+i);
	
	// controllo validità valori form
	
	valido = isNotEmpty(fields[0],nome) && valido;
	valido = isNotEmpty(fields[1],materiale) && valido;
	valido = isNotEmpty(fields[2],prezzo) && valido;
	if(valido) valido = isAPrice(prezzo) && valido;
		
	valido = isNotEmpty(fields[3],descrizione) && valido;	
	valido = isNotEmpty(fields[4],categoria) && valido;	
	
	// Controllo che almeno una taglia sia stata selezionata come disponibile
	
	var checkBoxTaglie=document.getElementsByName("taglie");
	valido = isCheckboxSelect(fields[5],checkBoxTaglie) && valido;
	
	
	// Controllo colori
	
	var checkBoxColori=document.getElementsByName("colors");
	valido = isCheckboxSelect(fields[6],checkBoxColori) && valido;
		
	// Controllo immagini
	
	var numImm = 3;
	for(iImm = 0; iImm < numImm; iImm++){
		var immagine = document.getElementById("immagine" + iImm).value;
		valido = isNotEmpty("Immagine" + iImm,immagine) && valido;
		if(valido) valido = isAPicture(iImm,immagine) && valido;
	}
	
	// Se l'errore non è già segnalato lo segnalo
	errorMesJs=document.getElementById('erroreFormJs');
	errorMesPerl=document.getElementById('erroreFormPerl');
	
	if(!valido && errorMesJs==null && errorMesPerl==null){
		
		var div = document.getElementById('contents');
			
		var p = document.createElement('p');
		p.setAttribute('id','jserror');
		p.setAttribute('class','msgerror');
		p.innerHTML='Errore nei dati inseriti ';
		
		var a = document.createElement('a');
		a.setAttribute('id','topAnchor');
		a.setAttribute('href','#title');
		a.innerHTML='Torna su';
		
		p.appendChild(a);
		if(!document.getElementById('jserror')) div.appendChild(p);
		
	}
	return valido;
	
};

