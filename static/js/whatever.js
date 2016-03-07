function doStuffOnload()
{
	if (isFontSizeDefined())
	{
		req_size = parseInt(localStorage.getItem('font_req_size'));
		applySizing(req_size);
	}

	if (localStorage.getItem('dyslexia_on'))
	{
		toggleDyslexia();
	}

	if (localStorage.getItem('high_contrast_on'))
	{
		toggleContrast();
	}
}
function showModal()
{
        $('#myModal').modal('show');
}
function toggleDyslexia()
{
	$('.btn').toggleClass("dyslexia");
	$('body').toggleClass("dyslexia");
	$('div').toggleClass("dyslexia");

	localStorage.setItem('dyslexia_on', "");
	if ($("body").hasClass("dyslexia"))
		localStorage.setItem('dyslexia_on', true);
}

function toggleContrast()
{
	$('.btn').toggleClass("high_contrast");
	$('input').toggleClass("high_contrast");
	$('textarea').toggleClass("high_contrast");
	$('body').toggleClass("high_contrast");
	$('#left_div').toggleClass("high_contrast");
	$('#right_div').toggleClass("high_contrast");
	$('#middle_div').toggleClass("high_contrast");
	$('#header_top').toggleClass("high_contrast");

	localStorage.setItem('high_contrast_on', "");
	if ($("body").hasClass("high_contrast"))
		localStorage.setItem('high_contrast_on', true);
}

function incFont()
{
	current_size = $('body').css('font-size');
	if (isFontSizeDefined())
		current_size = parseInt(localStorage.getItem('font_req_size'))

	req_size = parseInt(current_size) + 2;
	applySizing(req_size);
}

function decFont()
{
	current_size = $('body').css('font-size');
	if (isFontSizeDefined())
		current_size = parseInt(localStorage.getItem('font_req_size'))

	req_size = parseInt(current_size) - 2;
  applySizing(req_size);
}

function isFontSizeDefined()
{
	if (typeof localStorage.getItem('font_req_size') !== 'undefined')
		return true;
}

function applySizing(req_size)
{
  $('body').css('font-size', req_size);
  $('.btn').css('font-size', req_size);
  $('input').css('font-size', req_size);
	$('#sm_a').css('font-size', req_size - 2);
	$('#aa').css('font-size', req_size + 4);
  localStorage.setItem('font_req_size', req_size);
}

function deleteCollection(collection_id)
{
	ask=confirm("Are you sure you want to delete this collection? \n Items contained in this collection will be permanently lost");
    if(ask)
	{
		window.location="deleteCollection?id=" + collection_id;
	}
}

function editCollection(item_id, list_id)
{
	{
		window.location="/IAPTCollections/default/edit_item/" + item_id + "?list_id=" + list_id;
	}
}

function initTrade()
{
		$( "#sortable1, #sortable2" ).sortable({
			connectWith: ".connectedSortable"
		}).disableSelection();

		$( "#sortable3, #sortable4" ).sortable({
			connectWith: ".connectedSortable2"
		}).disableSelection();
}

function runAdvSearchScripts()
{
	// When Only search collection of clicked
	$("#only_one_user").change(function() {
		if(this.checked) {
			$('#my_collection').attr('checked', false);
			$('#all_collections').attr('checked', false);

			$('#single_collection_owner').attr('disabled', false);

		}	else {
			$('#only_one_user').attr('checked', false);
			$('#single_collection_owner').attr('disabled', true);
		}
	});

	// When my_collection or all_collections checked
	$("#my_collection, #all_collections").change(function() {
		if(this.checked) {
			$('#only_one_user').attr('checked', false);
			$('#single_collection_owner').attr('disabled', true);
		}
	});

	triggerAutoComplUsers();
}

function getItemAllInfo(item_id, list_id)
{
	info_page = window.location.origin + "/IAPTCollections/default/item_info_by_id.json?id=" + item_id;

	$.ajax({
	  url: info_page
	}).done(function(data ) {
		if (!data['info'][0]['image'])
			img_src = "/IAPTCollections/static/images/question.jpg";
		else
			img_src = "/IAPTCollections/default/download/" + data['info'][0]['image'];

		if (list_id == 0)
		{
			list_name = "collection";
		}
		else if (list_id == 1)
		{
			list_name = "have list";
		}
		else if (list_id == 2)
		{
			list_name = "wish list";
		}

		del_url = window.location.origin + "/IAPTCollections/default/delete_item/" + list_id + "/" + data['info'][0]['id'];

		new_html = "<div class='item_view'><img src='" + img_src ;
		new_html += "' alt='selected item image' class='item_view'><br>First Item</div>";
		new_html += "<div>Name: <b>" + data['info'][0]['name'] + "</b><br>";
		new_html += "<div>Value: <b>£" + data['info'][0]['price'] + "</b><br>";
		new_html += "<div>Owner: <b>" + data['owner'][0]['username'] + "</b><br>";
		new_html += "<div>Category: <b>" + data['info'][0]['type'] + "</b><br>";

		new_html += "<label for='description'>Description:</label>";
		new_html += "<textarea class='form-control' id='description' rows='8' disabled>" + data['info'][0]['description'] + "</textarea>";
		item_id = data['info'][0]['id'];
		new_html += "<button onclick='editCollection("+item_id+"," + list_id + ")' class='transp small_margins'><span class='glyphicon glyphicon-edit'></span>Edit item</button>";
		//						^ I need the 1 to be item_id but dont know how. Otherwise it should work.
		oncl =  "delItembyUrl('" + del_url + "')";

		new_html += "<button onclick=" + oncl + " class='transp small_margins'><span class='glyphicon glyphicon-trash'></span>Remove from " + list_name + "</button>";
		new_html += "</div>";

		$('#ajax_content_div').html(new_html);
	});
}

function addEnterListeners()
{
	$('#middle_div a').keydown( function(e) {
			var key = e.charCode ? e.charCode : e.keyCode ? e.keyCode : 0;
			if(key == 13) {
			 e.preventDefault();
				 $(this).click();
			}
	});
 }

function showLoginModal()
{
		$('#myModal').modal('show');
}

function redirIfAllowed(url)
{
	info_page = window.location.origin + "/IAPTCollections/default/logged_in.json"

	$.ajax({
	  url: info_page
	}).done(function(data ) {
		if (data['logged_in'] != null)
	{
		redir_url = window.location.origin + "/IAPTCollections/default/" + url;
		window.location.href = redir_url;
	}
	else
	{
		showLoginModal();
	}
	});
}

function redirToHome()
{
	window.location.href = window.location.origin + "/IAPTCollections/default/";
}

function delItembyUrl(url)
{
	$.ajax({
	  url: url
	}).done(function() {
		location.reload();
	});
}

function triggerAutoComplUsers()
{
	url = window.location.origin + "/IAPTCollections/default/all_users";
	$.ajax({
	  url: url
	}).done(function(data) {

		$("#single_collection_owner").autocomplete({
	      source: data
	    });
		});
}
